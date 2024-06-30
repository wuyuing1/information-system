from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from cryptography.fernet import Fernet
import bcrypt

from dblock import dblock

# 从数据库中获取用户信息
with dblock() as db:
    db.execute("SELECT user_sn, user_name FROM sys_user;")
    rows = db.fetchall()
    users = {int(row[0]): {"user_name": row[1]} for row in rows}
print(f"用户: {users}")

# 从数据库中获取用户密码
with dblock() as db:
    db.execute("SELECT user_sn, password FROM passwords;")
    rows = db.fetchall()
    user_passwords = {users.get(int(row[0]))["user_name"]: {"user_sn": int(row[0]), "password": row[1]} for row in rows}
print(f"密码: {user_passwords}")

app = FastAPI()
templates = Jinja2Templates(directory='./')

# 加密和解密的密钥
COOKIE_ENCRYPTION_KEY = Fernet.generate_key()
# COOKIE_ENCRYPTION_KEY = b'wabvJHHrgFsBPQMEpsV-eJdW0NjcG3NgRBWepnu8VnM='
print(f"COOKIE_ENCRYPTION_KEY = {COOKIE_ENCRYPTION_KEY}")
fernet = Fernet(COOKIE_ENCRYPTION_KEY)

@app.get("/")
async def main(request: Request):
    user_sn = get_current_user(request)
    if not user_sn:
        return RedirectResponse(url="/login", status_code=302)
    
    user_sn = int(user_sn)
    user = users.get(user_sn)
    print(f"user = {user}, type = {type(user)}")
    
    if not user:  
        return RedirectResponse(url="/error", status_code=302)
    
    return templates.TemplateResponse(
        "logined.html",
        {"request": request, "user": user["user_name"]},
        status_code=200
    )

@app.get("/login")
async def login_form_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
        status_code=200
    )

@app.post("/login")
async def login_action(username_input: str = Form(...), password_input: str = Form(...)):
    session_id = check_password(username_input, password_input)
    if session_id: 
        print(f"session_id = {session_id}")
        response = RedirectResponse(url="/", status_code=302)
        set_current_user(response, session_id)
        return response
    
    return RedirectResponse(url="/login", status_code=302)

@app.post("/logout")
async def handle_logout(response: Response):
    response = RedirectResponse(url="/login", status_code=302)
    set_current_user(response, None)
    return response

def get_current_user(request: Request):
    return get_secure_cookie(request, "session_id")

def get_secure_cookie(request: Request, name: str):
    value = request.cookies.get(name)
    if value is None:
        return None
    
    try:
        buffer = value.encode()
        secured_value = fernet.decrypt(buffer).decode()
        return secured_value
    except Exception:
        print("Cannot decrypt cookie value")
        return None

def check_password(username_input: str, password_input: str) -> str:
    principal = user_passwords.get(username_input)
    if principal is None:
        return None
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(principal.get("password").encode("utf-8"), salt).decode("utf-8")
    result = bcrypt.checkpw(password_input.encode("utf-8"), hashed.encode("utf-8"))
    
    if not result:
        return None
    
    session_id = principal.get("user_sn")
    return f"{session_id}"

def set_current_user(response: Response, session_id: str):
    if session_id is not None:
        set_current_cookie(response, "session_id", session_id)
    else:
        response.delete_cookie("session_id")

def set_current_cookie(response: Response, name: str, value: str, **kwargs):
    encrypted_value = fernet.encrypt(value.encode()).decode()
    response.set_cookie(name, encrypted_value, **kwargs)
