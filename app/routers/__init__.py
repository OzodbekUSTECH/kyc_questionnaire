from fastapi import FastAPI

from app.routers.surveys import router as surveys_router
from app.routers.admin import router as admin_router
from app.routers.files import router as files_router
from app.routers.answers import router as answers_router

all_routers = [
    surveys_router,
    admin_router,
    files_router,
    answers_router,
]


def register_routers(app: FastAPI, prefix: str = ""):
    """
    Initialize all routers in the app.
    """
    for router in all_routers:
        app.include_router(router, prefix=prefix)
