from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.core.config import settings

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    route_class=DishkaRoute,
)

templates = Jinja2Templates(directory="app/templates")


def verify_admin_credentials(username: str, password: str) -> bool:
    """Verify admin credentials against settings"""
    return username == settings.DOCS_USERNAME and password == settings.DOCS_PASSWORD


@router.get("/", response_class=HTMLResponse)
async def admin_panel(request: Request):
    """Serve the admin panel HTML"""
    return templates.TemplateResponse("admin.html", {"request": request})


@router.post("/login")
async def admin_login(request: Request):
    """Handle admin login"""
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
        
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required"
            )
        
        if not verify_admin_credentials(username, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        return {"message": "Login successful"}
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )
