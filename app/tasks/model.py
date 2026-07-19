# id, title, description, is_completed

from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.projects.model import Project


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    def __init__(
        self, is_completed: bool, title: str, project_id: int, description: str | None = None
    ):
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.project_id = project_id
