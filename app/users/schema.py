from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    email: str
    password: str

    model_config = {"extra": "forbid"}


class JWTResponse(BaseModel):
    token: str



class UserRegisterRequest(BaseModel):
    email: str
    password: str | None = None

    model_config = {"extra": "forbid"}


class UserRegisterResponse(BaseModel):
    id: int
    email: str
