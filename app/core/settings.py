from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, Request
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = "Board API"
    debug: bool = False


class DatabaseSettings(BaseModel):
    url: str


class AuthSettings(BaseModel):
    secret: str
    expire_minutes: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    database_url_sync: str
    jwt_secret: str
    jwt_expire_minutes: int

    @property
    def app(self) -> AppSettings:
        return AppSettings()

    @property
    def auth(self) -> AuthSettings:
        return AuthSettings(secret=self.jwt_secret, expire_minutes=self.jwt_expire_minutes)

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url)

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        parsed = urlparse(v)

        if parsed.scheme not in {"postgresql", "postgresql+asyncpg"}:
            raise ValueError("database_url scheme must be postgresql, postgresql+asyncpg")

        if not parsed.hostname:
            raise ValueError("database_url must include hostname")

        dbname = (parsed.path or "").lstrip("/")
        if not dbname:
            raise ValueError("database_url must include database")

        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("database_url port must be 1..65535")

        return v


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


SettingsDeps = Annotated[Settings, Depends(get_settings)]
