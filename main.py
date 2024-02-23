"""A Sample FastAPI Microservice"""

from enum import Enum
import logging

from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Response, status
from pydantic_settings import BaseSettings

import uvicorn

class Settings(BaseSettings):
    """Settings for TODO App"""
    app_title: str = "Todo API"
    app_summary: str = "A sample FastAPI for Todos"
    host: str = "localhost"
    port: int =  8000
    deploy_environment: str = "prod"

    if deploy_environment == "prod":
        IS_PROD: bool = True
    else:
        IS_PROD: bool = False


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

# shared data for now
todo_list = TodoList(
    title="Sample TODO List",
    todos=[
        Todo(id=1, title="Install Python", is_done=True),
        Todo(id=2, title="Create Microservice", is_done=False),
    ],
)

class Tags(Enum):
    """Tags to be used for documentation"""
    ROOT = "root"
    API = "API"

# #########################
# # SETUP the application #
# #########################
logger = logging.getLogger(__name__)
settings = Settings()
app = FastAPI(title=settings.app_title, summary=settings.app_summary)


@app.get("/status", tags=[Tags.ROOT])
async def get_status() -> DefaultMessage:
    """useful when using Docker or Kubernetes to see if the application is up"""
    return DefaultMessage(message= "OK")


@app.get("/", tags=[Tags.ROOT])
async def root() -> DefaultMessage:
    """Get for the root path, this is just a Hello World for now"""
    return DefaultMessage(message="Hello World!")


# All Todos
@app.get("/todos", tags=[Tags.API])
async def get_todos() -> TodoList:
    """Get a list of all todos"""
    return todo_list


# Single Todo
# Create
@app.post("/todo", tags=[Tags.API])
async def create_todo(todo: Todo, response: Response) -> TodoMessage:
    """Create a single todo"""
    if todo.id is None or todo.id == 0:
        # create a new id
        todo.id = len(todo_list.todos) + 1
        logger.debug("got id = None or 0, created new id %s", todo.id)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.error("got and id = %s, NOT ALLOWED", todo.id)
        return TodoMessage(todo=todo, message="Expecting 0 or None for id")

    # we passed checks
    todo_list.todos.append(todo)
    logger.debug("created a todo: %s ", todo)
    response.status_code = status.HTTP_200_OK
    return TodoMessage(todo=todo, message=f"Added new todo with id {todo.id}")


# Retrieve
@app.get("/todo/{todo_id}", tags=[Tags.API])
async def get_todo(todo_id: int, response: Response) -> TodoMessage:
    """Get a single todo"""
    for todo in todo_list.todos:
        if todo.id == todo_id:
            response.status_code = status.HTTP_200_OK
            return TodoMessage(todo=todo, message="OK")

    # we iterated through the list and didn't find the requested id
    response.status_code = status.HTTP_404_NOT_FOUND
    return TodoMessage(todo=None, message=f"Todo {todo_id} not found")


# Update
@app.put("/todo/{todo_id}", tags=[Tags.API])
async def put_todo(todo_update: Todo, todo_id: int, response: Response) -> TodoMessage:
    """Update a single todo"""
    if todo_update.id != 0 and todo_id != todo_update.id:
        logger.debug("Todo id %s does not match body id %s", todo_id, todo_update.id)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return TodoMessage(
            todo=None,
            message=f"Todo id from URL: {todo_id} does not match body id: {todo_update.id}",
        )

    for todo in todo_list.todos:
        if todo.id == todo_id:
            logger.debug("found a match for id %s, Updating", todo_id)
            response.status_code = status.HTTP_200_OK
            # we ignore the id from the body message and use the one passed in to the URL
            # we do not allow updating/changing the id
            if todo_update.is_done is not None:
                todo.is_done = todo_update.is_done
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.description is not None:
                todo.description = todo_update.description

            return TodoMessage(todo=todo, message=f"OK, updated Todo {todo_id}")

    # we iterated through the list and didn't find the requested id
    response.status_code = status.HTTP_404_NOT_FOUND
    return TodoMessage(todo=None, message=f"Todo {todo_id} not found")


# Delete
@app.delete("/todo/{todo_id}", tags=[Tags.API])
async def delete_todo(todo_id: int, response: Response) -> TodoMessage:
    """Delete a single todo"""
    for todo in todo_list.todos:
        if todo.id == todo_id:
            logger.debug("found a match for id %s, removing", todo_id)
            todo_list.todos.remove(todo)
            response.status_code = status.HTTP_200_OK
            return TodoMessage(todo=todo, message=f"Removed Todo {todo_id}")

    logger.error("Todo %s not found", todo_id)
    # we iterated through the list and didn't find the requested id
    response.status_code = status.HTTP_404_NOT_FOUND
    return TodoMessage(todo=None, message=f"Todo {todo_id} not found")


if __name__ == "__main__":
    # we only reload when not running in prod
    RELOAD = not settings.IS_PROD
    # start the application
    logger.debug(
        "Starting %s on %s:%s and reload:%s",
        settings.app_title,
        settings.host,
        settings.port,
        RELOAD,
    )

    uvicorn.run(app, host=settings.host, port=settings.port, reload=RELOAD)
