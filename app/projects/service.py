from typing import Annotated

from fastapi import Depends

from app.projects.model import Project
from app.projects.repository import (
    ProjectRepository,
    ProjectRepositoryDeps,
)
from app.projects.schema import ProjectCreateRequest, ProjectUpdateRequest


def get_project_serevice(repo: ProjectRepositoryDeps):
    return ProjectService(repo)


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def get(self, project_id: int, user_id: int):
        project = await self.repo.get_by_id(project_id)
        if project is None:
            return None
        member = await self.repo.get_member(project_id, user_id)
        if member is None:
            return None
        return project
        

    async def create(self, data: ProjectCreateRequest, user_id: int):
        project = Project(key=data.key, name=data.name, description=data.description)
        return await self.repo.save(project, user_id)

    async def update(self, project_id: int, data: ProjectUpdateRequest, user_id: int):
        project = await self.repo.get_by_id(project_id)

        if project is None:
            return None

        patch = data.model_dump(exclude_unset=True)
        for field, value in patch.items():
            setattr(project, field, value)
        return await self.repo.save(project, user_id)

    async def delete(self, project_id: int):
        project = await self.repo.get_by_id(project_id)
        if project is None:
            return False
        await self.repo.delete(project)
        return True


ProjectServiceDeps = Annotated[ProjectService, Depends(get_project_serevice)]
