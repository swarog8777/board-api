import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.projects.service import ProjectServiceDeps
from app.projects.schema import (
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectGetResponse,
    ProjectPath,
    ProjectUpdateRequest,
    ProjectUpdateResponse,
)
from app.users.current_user import CurrentUserDeps


router = APIRouter(prefix="/v1/projects", tags=["Projects"])
logger = logging.getLogger(__name__)

@router.get(
    "/{project_id}",
    response_model=ProjectGetResponse,
    description="""
    Получает проект по его ID
    если проекта нет возращает ошибку
    """,
)
async def get_project(
    service: ProjectServiceDeps,
    current_user: CurrentUserDeps,
    path: ProjectPath = Depends(),
):
    logger.info(current_user.email)
    project = await service.get(path.project_id, current_user.id)
    if project is None:
        raise HTTPException(404, "Project not found")
    return ProjectGetResponse(
        id=project.id, key=project.key, name=project.name, description=project.description
    )


@router.patch("/{project_id}", response_model=ProjectUpdateResponse)
async def update_project(
    service: ProjectServiceDeps,
    current_user: CurrentUserDeps,
    data: ProjectUpdateRequest, 
    path: ProjectPath = Depends()
):
    project = await service.update(path.project_id, data, current_user.id)
    if project is None:
        raise HTTPException(404, "Project not found")

    return ProjectUpdateResponse(
        id=project.id,
        key=project.key,
        name=project.name,
        description=project.description,
    )


@router.delete(
    "/{project_id}",
    description="""
    Удаляет проект по его ID
    если проекта нет возращает ошибку
    """,
)
async def delete_project(
    service: ProjectServiceDeps,
    path: ProjectPath = Depends(),
):
    success = await service.delete(path.project_id)
    if not success:
        raise HTTPException(404, "Project not found")


@router.post(
    "/",
    response_model=ProjectCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    service: ProjectServiceDeps, 
    data: ProjectCreateRequest,
    current_user: CurrentUserDeps
    ):
    res = await service.create(data, current_user.id)
    return ProjectCreateResponse(id=res.id, name=res.name)
