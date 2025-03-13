from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ✅ Login Page
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ✅ Logout Confirmation Page
@router.get("/logout", response_class=HTMLResponse)
def logout_page(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})
