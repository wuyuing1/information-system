from aiohttp import web
from serv.json_util import json_response, json_error
from .config import web_routes
from .dblock import dblock


@web_routes.get("/api/select/check")
async def check_selection(request):
    student_id = request.query.get("studentId")
    course_id = request.query.get("courseId")
    ban_id = request.query.get("banId")
    with dblock() as db:
        db.execute(
            """
            SELECT COUNT(*) FROM course_select
            WHERE student_id = %(student_id)s AND course_id = %(course_id)s AND ban_id = %(ban_id)s;
            """,
            dict(student_id=student_id, course_id=course_id, ban_id=ban_id),
        )
        row = db.fetchone()
        if row.count > 0:
            record = True
        else:
            record = False

    return json_response({"isAlreadySelected": record})


@web_routes.get("/api/select/status/{stuSn:\d+}")
async def get_selection_status(request):
    student_no = request.match_info.get("stuSn")

    with dblock() as db:
        db.execute(
            """
            SELECT s.sn, student_id, course_id, ban_id FROM course_select as cs
            INNER JOIN student as s ON s.no = cs.student_id
            WHERE s.sn =%(student_no)s ;
            """,
            dict(student_no=student_no),
        )
        rows = db.fetchall()

        selection_status = [{
            "studentSn": row.sn,
            "courseId": row.course_id,
            "banId": row.ban_id
        } for row in rows]

    return json_response(selection_status)


@web_routes.post("/api/select/enroll")
async def enroll_course(request):
    data = await request.json()
    student_id = data.get("studentId")
    course_id = data.get("courseId")
    ban_id = data.get("banId")

    with dblock() as db:
        db.execute(
            """
            INSERT INTO course_select (student_id, course_id, ban_id)
            VALUES (%(student_id)s, %(course_id)s, %(ban_id)s);
            """,
            dict(student_id=student_id, course_id=course_id, ban_id=ban_id),
        )

    return web.Response(text="", content_type="text/plain")


@web_routes.post("/api/select/deselect")
async def deselect_course(request):
    data = await request.json()
    student_id = data.get("studentId")
    course_id = data.get("courseId")
    ban_id = data.get("banId")

    with dblock() as db:
        db.execute(
            """
            DELETE FROM course_select
            WHERE student_id = %(student_id)s AND course_id = %(course_id)s AND ban_id = %(ban_id)s;
            """,
            dict(student_id=student_id, course_id=course_id, ban_id=ban_id),
        )

    return web.Response(text="", content_type="text/plain")