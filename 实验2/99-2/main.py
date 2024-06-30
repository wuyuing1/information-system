import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
async def default_size(request: Request):
    response = await render_grid(request, size="9x9")
    return response
@app.get("/{size}")
async def grid_size(request: Request, size: str):
    response = await render_grid(request, size)
    return response


async def render_grid(request: Request, size: str):
    matched = re.match(r"(?P<n>\d+)(?:[xX](?P<m>\d+))?", size)
    if matched:
        n, m = matched.group("n"), matched.group("m")
        n = int(n) if n else 9
        m = int(m) if m else 9
    else:
        return HTTPException(status_code=400, detail=f"无法识别size: '{size}'")

    ctx = dict(request=request, n=n, m=m)
    return templates.TemplateResponse("grid.html", ctx)