from aiohttp import web
import datetime
from serv.json_util import json_response, json_error
from .config import web_routes
from .dblock import dblock


@web_routes.get("/api/student/list")
async def get_student_list(request):
    with dblock() as db:
        db.execute("""
        SELECT s.sn as stu_sn,
            s.no as stu_no,
            s.name as stu_name, 
            s.gender as stu_gender,
            s.enrolled as stu_enroll_date,
            s.academy as stu_academy,
            s.grade as stu_grade,
            s.class_ as stu_class
        FROM student as s
        ORDER BY stu_sn;        
        """)
        data = list(db)

    return json_response(data)


@web_routes.post("/api/student")
async def new_student(request):
    student = await request.json()
    if not student.get('enrolled'):
        student['enrolled'] = datetime.date(1900, 1, 1)

    stu_no = student.get("stu_no")
    if not isinstance(stu_no, str) or len(stu_no.strip()) != 4:
        return json_error(f"学号'{stu_no}'需按照4位学号编制")

    with dblock() as db:
        db.execute(
            """
        SELECT sn AS stu_sn, name AS stu_name FROM student
        WHERE no=%(stu_no)s
        """, dict(stu_no=stu_no))
        record = db.fetchone()
        if record:
            return json_error(
                f"学号'{stu_no}'已被占用: {record.stu_name} (#{record.stu_sn})")

    with dblock() as db:
        db.execute(
        """
        INSERT INTO student (no, name, gender, enrolled, academy, grade, class_)
        VALUES(%(stu_no)s, %(stu_name)s, %(gender)s, %(enrolled)s, %(academy)s, %(grade)s, %(class_)s) RETURNING sn;
        """, student)
        record = db.fetchone()

        student["stu_sn"] = record.sn

    return json_response(student)


@web_routes.get("/api/student/{stu_sn:\d+}")
async def get_student_profile(request):
    stu_sn = request.match_info.get("stu_sn")

    with dblock() as db:
        db.execute(
        """
        SELECT sn AS stu_sn, no AS stu_no, name AS stu_name, gender, enrolled, academy, grade, class_ FROM student
        WHERE sn=%(stu_sn)s
        """, dict(stu_sn=stu_sn))
        record = db.fetchone()

    if record is None:
        return web.HTTPNotFound(text=f"no such student: stu_sn={stu_sn}")

    return json_response(record)


@web_routes.put("/api/student/{stu_sn:\d+}")
async def update_student(request):
    stu_sn = request.match_info.get("stu_sn")

    student = await request.json()
    if not student.get('enrolled'):
        student['enrolled'] = datetime.date(1900, 1, 1)

    student["stu_sn"] = stu_sn

    with dblock() as db:
        db.execute(
            """
        UPDATE student SET
            no=%(stu_no)s, name=%(stu_name)s, gender=%(gender)s, enrolled=%(enrolled)s, academy=%(academy)s, grade=%(grade)s, class_=%(class_)s
        WHERE sn=%(stu_sn)s;
        """, student)

    return json_response(student)


@web_routes.delete("/api/student/{stu_sn:\d+}")
async def delete_student(request):
    stu_sn = request.match_info.get("stu_sn")

    with dblock() as db:
        db.execute(
            """
        DELETE FROM student WHERE sn=%(stu_sn)s;
        """, dict(stu_sn=stu_sn))

    return web.Response(text="", content_type="text/plain")