"""A Sample FastAPI Microservice"""

import logging.config

from fastapi import FastAPI, HTTPException, Depends, Response, status
from fastapi.responses import JSONResponse
from typing import Optional

import uvicorn

from config import Settings, LogConfig
from models import Tags, TodoList, Todo, TodoMessage, DefaultMessage

# Initialize configuration
settings = Settings()
log_config = LogConfig()
log_config.configure()

# Initialize logger
logger = logging.getLogger("todo_app")

app = FastAPI(title=settings.title, summary=settings.summary)

# Shared data (should be replaced with DB in production)
todo_list = TodoList(
    title="Sample TODO List",
    todos=[
        Todo(id=1, title="Install Python", is_done=True),
        Todo(id=2, title="Create Microservice", is_done=False),
    ],
)

# #########################
# # SETUP the application #
# #########################
def get_settings():
    return settings

@app.get("/status")
async def get_status():
    """useful when using Docker or Kubernetes to see if the application is up"""
    return DefaultMessage(message="OK")

@app.get("/")
async def root():
    """Get for the root path, this is just a Hello World for now"""
    return DefaultMessage(message="Hello World!")

@app.get("/todos", tags=[Tags.API])
async def get_todos() -> TodoList:
    """Get a list of all todos"""
    return todo_list

# Create
@app.post("/todo", tags=[Tags.API])
async def create_todo(todo: Todo, response: Response) -> TodoMessage:
    """Create a single todo"""
    if todo.id in (None, 0):
        # create a new id
        todo.id = len(todo_list.todos) + 1
        logger.debug("got id = None or 0, created new id %s", todo.id)
    else:
        logger.error("got an id = %s, NOT ALLOWED", todo.id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID must be 0 or None")

    # we passed checks
    todo_list.todos.append(todo)
    logger.debug("created a todo: %s ", todo)
    response.status_code = status.HTTP_201_CREATED
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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo {todo_id} not found")

# Update
@app.put("/todo/{todo_id}", tags=[Tags.API])
async def put_todo(todo_update: Todo, todo_id: int, response: Response) -> TodoMessage:
    """Update a single todo"""
    if todo_update.id != 0 and todo_id != todo_update.id:
        logger.debug("Todo id %s does not match body id %s", todo_id, todo_update.id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Todo id from URL: {todo_id} does not match body id: {todo_update.id}")

    for todo in todo_list.todos:
        if todo.id == todo_id:
            logger.debug("found a match for id %s, Updating", todo_id)
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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo {todo_id} not found")

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

    # we iterated through the list and didn't find the requested id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo {todo_id} not found")

if __name__ == "__main__":
    RELOAD = not settings.IS_PROD
    uvicorn.run(app, host=settings.host, port=settings.port, reload=RELOAD)
