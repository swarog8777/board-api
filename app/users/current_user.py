from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.users.jwt import decode_access_token
from app.users.model import User
from app.users.service import UserServiceDeps

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: UserServiceDeps
) -> User:
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(401, "Invalid token")
    user = await service.get(user_id)
    if user is None:
        raise HTTPException(401, "User not found")
    return user

CurrentUserDeps = Annotated[User, Depends(get_current_user)]