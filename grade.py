from aiohttp import web
# from dataclasses import asdict
from serv.json_util import json_dumps

from .config import web_routes
from .dblock import dblock

@web_routes.get("/api/grade/list")
async def get_grade_list(request):
    course = request.match_info.get("course")
    with dblock() as db:
        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE c.name=%(course)s    
        ORDER BY stu_sn, cou_sn;        
        """)
        data = list(db)

    return web.Response(text=json_dumps(data), content_type="application/json")
