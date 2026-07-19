

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.projects.model import ProjectMember

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    project_members: Mapped[list["ProjectMember"]] = relationship(
        "ProjectMember", back_populates="user"
    )

    def __init__(self, email: str, hashed_password: str, is_active: bool = True):
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active