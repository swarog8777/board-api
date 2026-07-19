from typing import Annotated

from fastapi import Depends
from sqlalchemy import func, select
#from sqlalchemy.sql.functions import count

from app.core.db import DBSessionDeps
from app.tasks.model import Task


class TaskRepository:
    def __init__(self, session: DBSessionDeps):
        self.session = session

    async def get_by_id(self, task_id: int):
        return await self.session.get(Task, task_id)

    async def save(self, task: Task):
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def search(self, offset: int = 0, limit: int = 20, project_id: int | None = None):
        count_query = select(func.count()).select_from(Task)
        query = select(Task)
        if project_id is not None:
            count_query = count_query.where(Task.project_id == project_id)
            query = query.where(Task.project_id == project_id)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(Task.id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        tasks = list(result.scalars().all())
        return tasks, total

def get_task_repository(session: DBSessionDeps):
    return TaskRepository(session)


TaskRepositoryDeps = Annotated[TaskRepository, Depends(get_task_repository)]
