from aiohttp import web
from serv.json_util import json_response, json_error
from .config import web_routes
from .dblock import dblock


@web_routes.get("/api/course/list")
async def get_course_list(request):
    with dblock() as db:
        db.execute("""
        SELECT c.sn as course_sn,
            c.no as course_no,
            c.name as course_name,
            c.xueqi as course_xueqi,
            c.credit as course_credit,
            c.time as course_time,
            c.teacher as course_teacher,
            c.banci as course_banci,
            c.shijian as course_shijian,
            c.didian as course_didian
        FROM course as c
        ORDER BY course_sn;        
        """)
        data = list(db)

    return json_response(data)


@web_routes.post("/api/course")
async def new_course(request):
    course = await request.json()

    # 检查新建课程的课程号是否符合规则，是否已经存在
    cou_no = course.get("cou_no")
    if not isinstance(cou_no, str) or len(cou_no.strip()) != 3:
        return json_error(f"课程号'{cou_no}'需按照3位课程号编制")

    with dblock() as db:
        db.execute(
        """
        SELECT sn AS cou_sn, name AS cou_name FROM course
        WHERE no=%(cou_no)s
        """, dict(cou_no=cou_no))
        record = db.fetchone()
        if record:
            return json_error(
                f"课程号'{cou_no}'已被占用: {record.cou_name} (#{record.cou_sn})")

    with dblock() as db:
        db.execute(
            """
        INSERT INTO course (no, name ,xueqi ,credit ,time ,teacher, banci, didian, shijian)
        VALUES(%(cou_no)s, %(cou_name)s ,%(xueqi)s ,%(credit)s ,%(time)s ,%(teacher)s, %(banci)s, %(didian)s, %(shijian)s) RETURNING sn;
        """, course)
        record = db.fetchone()

        course["cou_sn"] = record.sn

    return json_response(course)


@web_routes.get("/api/course/{cou_sn:\d+}")
async def get_course_profile(request):
    cou_sn = request.match_info.get("cou_sn")

    with dblock() as db:
        db.execute(
            """
        SELECT sn AS cou_sn, no AS cou_no, name AS cou_name ,xueqi ,credit ,time ,teacher, banci, didian, shijian FROM course
        WHERE sn=%(cou_sn)s
        """, dict(cou_sn=cou_sn))
        record = db.fetchone()

    if record is None:
        return web.HTTPNotFound(text=f"no such course: cou_sn={cou_sn}")

    return json_response(record)


@web_routes.put("/api/course/{cou_sn:\d+}")
async def update_course(request):
    cou_sn = request.match_info.get("cou_sn")

    course = await request.json()

    course["cou_sn"] = cou_sn

    with dblock() as db:
        db.execute(
            """
        UPDATE course SET
            no=%(cou_no)s, name=%(cou_name)s,xueqi=%(xueqi)s ,credit=%(credit)s ,time=%(time)s ,teacher=%(teacher)s, banci=%(banci)s, didian=%(didian)s, shijian=%(shijian)s
        WHERE sn=%(cou_sn)s;
        """, course)

    return json_response(course)


@web_routes.delete("/api/course/{cou_sn:\d+}")
async def delete_course(request):
    cou_sn = request.match_info.get("cou_sn")

    with dblock() as db:
        db.execute(
        """
        DELETE FROM course WHERE sn=%(cou_sn)s;
        """, dict(cou_sn=cou_sn))

    return web.Response(text="", content_type="text/plain")