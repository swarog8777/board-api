from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from app.core.db import DBSessionDeps
from app.users.model import User


class UserRepository:
    def __init__(self, session: DBSessionDeps):
        self.session = session

    async def get_by_id(self, user_id: int):
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def save(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


def get_user_repository(session: DBSessionDeps):
    return UserRepository(session)


UserRepositoryDeps = Annotated[UserRepository, Depends(get_user_repository)]
