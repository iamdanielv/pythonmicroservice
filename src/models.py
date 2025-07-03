"""Models for TODO API"""

from enum import Enum

from pydantic import BaseModel, field_validator


class Tags(Enum):
    """Tags to be used for documentation"""

    APP_NAME = "TODOAPP"
    ROOT = "root"
    API = "API"


class Todo(BaseModel):
    """A Todo item"""

    id: int | None = 0
    title: str
    description: str | None = ""
    is_done: bool | None = False

    @field_validator("id")
    @classmethod
    def id_must_be_positive(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("ID must be 0 or greater")
        return v


class TodoMessage(BaseModel):
    """A Todo Message"""

    todo: Todo | None
    message: str


class TodoList(BaseModel):
    """Holds a Todo List"""

    title: str
    todos: list[Todo]


class DefaultMessage(BaseModel):
    """A Default message"""

    message: str
