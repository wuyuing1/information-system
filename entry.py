from aiohttp import web
from serv.json_util import json_response, json_error
from .config import web_routes
from .dblock import dblock


@web_routes.get("/api/entry/list/{cou_sn:\d+}")
async def get_entry_list(request):
    cou_sn = request.match_info.get("cou_sn")
    with dblock() as db:
        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, c.banci as cou_banci, 
            g.grade 
        FROM course_grade as g
            LEFT JOIN student as s ON s.sn = g.stu_sn 
            LEFT JOIN course as c ON c.sn = g.cou_sn 
            LEFT JOIN course_select as cs ON cs.course_id = c.no 
        WHERE cou_sn=%(cou_sn)s        
        """, dict(cou_sn=cou_sn))
        data = list(db)

    return json_response(data)


@web_routes.post("/api/entry")
async def entry(request):
    data = await request.json()
    studentName = data.get("studentName")
    grade = data.get("grade")
    courseId = data.get("courseId")

    with dblock() as db:
        db.execute("""
        SELECT sn
        FROM student
        WHERE name=%(name)s        
        """, dict(name=studentName))
        row = db.fetchone()

    with dblock() as db2:
        db2.execute(
        """
        INSERT INTO course_grade (stu_sn, cou_sn, grade)
        VALUES (%(student_id)s, %(course_id)s, %(grade)s); 
        """, dict(student_id=row.sn, course_id=courseId, grade=grade))


    return json_response({"message": "Entry successful"})