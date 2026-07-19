import logging

from app.core.middleware import TimingMiddleware
from app.core.settings import Settings
from app.projects.routes import router as project_router
from app.tasks.routes import router as task_router
from app.users.routes import router as user_router
from fastapi import FastAPI

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    logger.debug("Запуск приложения")
    settings = Settings()  # type: ignore[call-arg]
    new_app = FastAPI(
        title=settings.app.name,
        description="API аналог jira",
        version="0.1.1",
        openapi_tags=[
            {"name": "Projects", "description": "Управление проектами"},
            {"name": "Tasks", "description": "Управление задачами"},
            {"name": "Auth", "description": "Авторизация пользователя"},
        ],
    )

    new_app.state.settings = settings
    new_app.include_router(project_router)
    new_app.include_router(task_router)
    new_app.include_router(user_router)
    new_app.add_middleware(TimingMiddleware)
    return new_app


app = create_app()
