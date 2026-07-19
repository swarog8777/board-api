import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from app.core.db import DBSessionDeps
from app.projects.model import Project, ProjectMember

logger = logging.getLogger(__name__)


class ProjectRepository:
    def __init__(self, session: DBSessionDeps):
        self.session = session

    async def get_by_id(self, project_id: int):
        return await self.session.get(Project, project_id)
    
    async def get_member(self, project_id: int, user_id: int) -> ProjectMember | None:
        result = await self.session.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()


    async def save(self, project: Project, user_id: int):
        self.session.add(project)
        await self.session.flush()
        member = ProjectMember(
            user_id=user_id,
            project_id=project.id,
            role="owner"
        )
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete(self, project: Project):
        await self.session.delete(project)
        await self.session.commit()


def get_project_repository(session: DBSessionDeps):
    return ProjectRepository(session)


ProjectRepositoryDeps = Annotated[ProjectRepository, Depends(get_project_repository)]
