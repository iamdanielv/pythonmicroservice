"""Todo API Router"""

import logging

from fastapi import APIRouter, HTTPException, Response, status

from src.models import Todo, TodoList, TodoMessage

logger = logging.getLogger("todo_app")
router = APIRouter()

# Shared data (should be replaced with DB in production)
todo_list = TodoList(
    title="Sample TODO List",
    todos=[
        Todo(
            id=1,
            title="Setup Python",
            description="Get your Python environment ready",
            is_done=True,
        ),
        Todo(
            id=2,
            title="Build a Microservice",
            description="something about building a microservice",
            is_done=False,
        ),
    ],
)


@router.get("/todos")
async def get_todos() -> TodoList:
    """Get a list of all todos"""
    return todo_list


# Create
@router.post("/todo")
async def create_todo(todo: Todo, response: Response) -> TodoMessage:
    """Create a single todo"""
    if todo.id in (None, 0):
        # create a new id
        todo.id = len(todo_list.todos) + 1
        logger.debug("got id = None or 0, created new id %s", todo.id)
    else:
        logger.error("got an id = %s, NOT ALLOWED", todo.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID must be 0 or None",
        )

    # we passed checks
    todo_list.todos.append(todo)
    logger.debug("created a todo: %s ", todo)
    response.status_code = status.HTTP_201_CREATED
    return TodoMessage(todo=todo, message=f"Added new todo with id {todo.id}")


# Retrieve
@router.get("/todo/{todo_id}")
async def get_todo(todo_id: int, response: Response) -> TodoMessage:
    """Get a single todo"""
    if todo_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID must be a positive integer",
        )

    for todo in todo_list.todos:
        if todo.id == todo_id:
            response.status_code = status.HTTP_200_OK
            return TodoMessage(todo=todo, message="OK")

    # we iterated through the list and didn't find the requested id
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo {todo_id} not found",
    )


# Update
@router.put("/todo/{todo_id}")
async def put_todo(
    todo_update: Todo, todo_id: int, response: Response
) -> TodoMessage:
    """Update a single todo"""
    if todo_update.id != 0 and todo_id != todo_update.id:
        logger.debug(
            "Todo id %s does not match body id %s", todo_id, todo_update.id
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Todo id from URL: {todo_id} does not match body id: "
            f"{todo_update.id}",
        )

    for todo in todo_list.todos:
        if todo.id == todo_id:
            logger.debug("found a match for id %s, Updating", todo_id)
            # we ignore the id from the body message
            # and use the one passed in to the URL
            # we do not allow updating/changing the id
            if todo_update.is_done is not None:
                todo.is_done = todo_update.is_done
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.description is not None:
                todo.description = todo_update.description
            return TodoMessage(todo=todo, message=f"OK, updated Todo {todo_id}")

    # we iterated through the list and didn't find the requested id
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo {todo_id} not found",
    )


# Delete
@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, response: Response) -> TodoMessage:
    """Delete a single todo"""
    for todo in todo_list.todos:
        if todo.id == todo_id:
            logger.debug("found a match for id %s, removing", todo_id)
            todo_list.todos.remove(todo)
            response.status_code = status.HTTP_200_OK
            return TodoMessage(todo=todo, message=f"Removed Todo {todo_id}")

    # we iterated through the list and didn't find the requested id
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo {todo_id} not found",
    )
