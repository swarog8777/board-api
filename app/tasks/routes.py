import logging
from fastapi import APIRouter, Depends, status

from .service import TaskServiceDeps

from .schema import TaskCreateRequest, TaskCreateResponse, TaskGetResponse, TaskPath, TaskSearchParams, TaskSearchResponse


router = APIRouter(prefix="/v1/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)


@router.get(
    "/{task_id}",
    response_model=TaskGetResponse,
    description="""
    Получает задачу по его ID
    если задачи нет возращает ошибку
    """,
)
async def get_task(
    service: TaskServiceDeps,
    path: TaskPath = Depends(),
):
    res = await service.get(path.task_id)
    return TaskGetResponse(
        id=res.id,
        title=res.title,
        description=res.description,
        is_completed=res.is_completed,
        project_id=res.project_id,
    )

@router.get(
    "/",
    response_model=TaskSearchResponse,
    description="""
    Поиск задачи
    """,
)
async def search_tasks(
    service: TaskServiceDeps,
    params: TaskSearchParams = Depends(),
):
    tasks, total = await service.search(params)
    return TaskSearchResponse(
        items=[TaskGetResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            is_completed=t.is_completed,
            project_id=t.project_id
        )
        for t in tasks
        ],
        total=total,
        limit=params.limit,
        offset=params.offset
    )

@router.post(
    "/",
    response_model=TaskCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(service: TaskServiceDeps, data: TaskCreateRequest):
    res = await service.create(data)
    return TaskCreateResponse(
        id=res.id,
        title=res.title,
        description=res.description,
        is_completed=res.is_completed,
        project_id=res.project_id,
    )
