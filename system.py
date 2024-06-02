from aiohttp import web
import datetime
from serv.json_util import json_result, json_fail
from .config import web_routes
from .dblock import db_connect

@web_routes.get("/api/student_info/list")
async def get_student_list(request):
    with db_connect() as db:
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

    return json_result(data)

@web_routes.post("/api/student_info")
async def new_student(request):
    student_info = await request.json()
    if not student_info.get('enrolled'):
        student_info['enrolled'] = datetime.date(1900, 1, 1).isoformat()

    stu_no = student_info.get("stu_no")
    if not isinstance(stu_no, str) or len(stu_no.strip()) != 4:
        return json_fail(f"学号'{stu_no}'需按照4位学号编制")

    with db_connect() as db:
        db.execute(
            """
        SELECT sn AS stu_sn, name AS stu_name FROM student
        WHERE no=%(stu_no)s
        """, dict(stu_no=stu_no))
        record = db.fetchone()
        if record:
            return json_fail(
                f"学号'{stu_no}'已被占用: {record.stu_name} (#{record.stu_sn})")

    with db_connect() as db:
        db.execute(
        """
        INSERT INTO student (no, name, gender, enrolled, academy, grade, class_)
        VALUES(%(stu_no)s, %(stu_name)s, %(gender)s, %(enrolled)s, %(academy)s, %(grade)s, %(class_)s) RETURNING sn;
        """, student_info)
        record = db.fetchone()

        student_info["stu_sn"] = record.sn

    return json_result(student_info)