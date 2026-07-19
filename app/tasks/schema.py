from pydantic import BaseModel, Field


class TaskPath(BaseModel):
    task_id: int = Field(gt=0)


class TaskGetResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    project_id: int
    is_completed: bool


class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = None
    project_id: int

    model_config = {"extra": "forbid"}


class TaskCreateResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    project_id: int
    is_completed: bool


class TaskSearchParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
    project_id: int | None = Field(None, gt=0)


class TaskSearchResponse(BaseModel):
    items: list[TaskGetResponse]
    total: int
    limit: int
    offset: int