from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router=APIRouter()
templates=Jinja2Templates(directory="app/templates")

def page(name):
    async def handler(request: Request): return templates.TemplateResponse(name,{"request":request})
    return handler

router.add_api_route("/", page("index.html"), response_class=HTMLResponse)
router.add_api_route("/login", page("login.html"), response_class=HTMLResponse)
router.add_api_route("/register", page("register.html"), response_class=HTMLResponse)
router.add_api_route("/dashboard", page("dashboard.html"), response_class=HTMLResponse)
