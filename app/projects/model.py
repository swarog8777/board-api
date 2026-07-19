from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.users.model import User

if TYPE_CHECKING:
    from app.tasks.model import Task


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan", passive_deletes=True
    )
    members: Mapped[list["ProjectMember"]] = relationship(
        "ProjectMember", back_populates="project"
    )
    def __init__(self, key: str, name: str | None = None, description: str | None = None):
        self.key = key
        self.name = name
        self.description = description


class ProjectMember(Base):
    __tablename__ = "project_members"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str] = mapped_column(String(50), default="member")
    user: Mapped["User"] = relationship(
        "User", back_populates="project_members"
    )
    project: Mapped["Project"] = relationship(
        "Project", back_populates="members"
    )

    def __init__(self, user_id: int, project_id: int, role: str):
        self.user_id = user_id
        self.project_id = project_id
        self.role = role