"""Models for TODO API"""

from enum import Enum

from pydantic import BaseModel, model_validator


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

    @classmethod
    @model_validator(mode="before")
    def check_id(cls, values: dict) -> dict:
        if values.get("id") is not None and values.get("id") < 0:
            raise ValueError("ID must be 0 or greater")
        return values


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
