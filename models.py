"""Models for TODO API"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class Tags(Enum):
    """Tags to be used for documentation"""
    APP_NAME = "TODOAPP"
    ROOT = "root"
    API = "API"


class Todo(BaseModel):
    """A Todo item"""

    id: Optional[int] | None = 0
    title: str
    description: Optional[str] | None = ""
    is_done: bool | None = False


class TodoMessage(BaseModel):
    """A Todo Message"""

    todo: Optional[Todo]
    message: str


class TodoList(BaseModel):
    """Holds a Todo List"""

    title: str
    todos: List[Todo]


class DefaultMessage(BaseModel):
    """A Default message"""

    message: str
