from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.di.containers import app_container
from app.exceptions.register import register_exceptions
from app.middlewares import register_middlewares

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles  # добавлено для статики

from app.routers import register_routers

from app.utils.dependencies import get_current_user_for_docs




def create_app():
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    setup_dishka(app_container, app)
    register_middlewares(app)
    register_exceptions(app)
    register_routers(app)

    # Настройка отдачи файлов из папки uploads по адресу /uploads
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    return app


app = create_app()


templates = Jinja2Templates(directory="app/templates")


@app.get("/", include_in_schema=False)
async def root(request: Request):
    """User dashboard"""
    return templates.TemplateResponse("user_dashboard.html", {"request": request})


@app.get("/survey/{survey_id}", include_in_schema=False)
async def survey_page(request: Request, survey_id: str):
    """Survey page"""
    return templates.TemplateResponse("user_survey.html", {
        "request": request,
        "survey_id": survey_id
    })


@app.get(
    "/api/docs",
    include_in_schema=False,
    dependencies=[Depends(get_current_user_for_docs)],
)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="QUESTIONNAIRE API",
        swagger_ui_parameters={"docExpansion": "none"},
    )


@app.get(
    "/api/openapi.json",
    include_in_schema=False,
    dependencies=[Depends(get_current_user_for_docs)],
)
async def get_open_api_endpoint():
    openapi_schema = get_openapi(
        title="QUESTIONNAIRE API", version="1.0.0", routes=app.routes
    )
    openapi_schema["servers"] = [
        {"url": "/", "description": "Base Path for API"},
    ]
    return openapi_schema
