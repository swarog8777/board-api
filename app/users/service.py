import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from app.users.jwt import create_access_token
from app.users.model import User
from app.users.schema import UserLoginRequest, UserRegisterRequest
from app.users.security import hash_password, verify_password

from .repository import (
    UserRepository,
    UserRepositoryDeps,
)

logger = logging.getLogger(__name__)


def get_user_serevice(user_repo: UserRepositoryDeps):
    return UserService(user_repo)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get(self, user_id: int):
        return await self.user_repo.get_by_id(user_id)


    async def create(self, data: UserRegisterRequest):
        user = await self.user_repo.get_by_email(data.email)
        if user:
            raise HTTPException(400, "User already exist")
        hashed = hash_password(data.password)
        user = User(email=data.email, hashed_password=hashed)        
        saved_user = await self.user_repo.save(user)
        return create_access_token(saved_user.id)
        
    
    async def authenticate(self, data: UserLoginRequest):
        user = await self.user_repo.get_by_email(data.email)
        if user is None:
            return None
        if not verify_password(data.password, user.hashed_password):
            return None
        return create_access_token(user.id)


UserServiceDeps = Annotated[UserService, Depends(get_user_serevice)]
