# test_todo.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from src.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_status():
    response = client.get("/status")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "OK"}

@pytest.mark.asyncio
async def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World!"}

@pytest.mark.asyncio
async def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

@pytest.mark.asyncio
async def test_create_todo():
    response = client.post("/todo", json={"title": "New Task"})
    assert response.status_code == status.HTTP_201_CREATED
    assert "Added new todo with id" in response.json()["message"]

@pytest.mark.asyncio
async def test_create_todo_invalid_id():
    response = client.post("/todo", json={"id": 1, "title": "Invalid ID"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "ID must be 0 or None" in response.text

@pytest.mark.asyncio
async def test_get_todo():
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "OK"

@pytest.mark.asyncio
async def test_get_todo_not_found():
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Todo 999 not found" in response.text

@pytest.mark.asyncio
async def test_update_todo():
    response = client.put("/todo/1", json={"title": "Updated Task"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "OK, updated Todo 1"

@pytest.mark.asyncio
async def test_update_todo_invalid_id():
    response = client.put("/todo/1", json={"id": 2, "title": "Invalid ID"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Todo id from URL: 1 does not match body id: 2" in response.text

@pytest.mark.asyncio
async def test_delete_todo():
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Removed Todo 1"

@pytest.mark.asyncio
async def test_delete_nonexistent_todo():
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert "Todo 999 not found" in response.text

@pytest.mark.asyncio
async def test_update_todo_description():
    # Add a new todo first
    response = client.post("/todo", json={"title": "Task with Description"})
    assert response.status_code == status.HTTP_201_CREATED
    # get the id of the newly created todo
    todo_id = response.json()["todo"]["id"]
    # update the description
    response = client.put(f"/todo/{todo_id}", json={"id" : todo_id, "title": "Updated Task", "description": "New Description"})
    assert response.status_code == status.HTTP_200_OK
    assert "OK, updated Todo" in response.json()["message"]
    assert response.json()["todo"]["description"] == "New Description"

@pytest.mark.asyncio
async def test_create_todo_negative_id():
    response = client.post("/todo", json={"id": -1, "title": "Invalid ID"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "ID must be 0 or None" in response.text

@pytest.mark.asyncio
async def test_create_todo_invalid_id_type():
    response = client.post("/todo", json={"id": "invalid", "title": "Invalid ID"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Input should be a valid integer" in response.text

@pytest.mark.asyncio
async def test_get_todo_zero():
    response = client.get("/todo/0")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Todo 0 not found" in response.text

@pytest.mark.asyncio
async def test_update_todo_zero():
    response = client.put("/todo/0", json={"title": "Updated Zero"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Todo 0 not found" in response.text

@pytest.mark.asyncio
async def test_get_todo_string_id():
    response = client.get("/todo/abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Input should be a valid integer" in response.text

@pytest.mark.asyncio
async def test_update_todo_invalid_id():
    response = client.put("/todo/1", json={"id": 2, "title": "Invalid ID"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Todo id from URL: 1 does not match body id: 2" in response.text

@pytest.mark.asyncio
async def test_update_todo_string_id():
    response = client.put("/todo/1", json={"id": "abc", "title": "Invalid ID"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Input should be a valid integer" in response.text

@pytest.mark.asyncio
async def test_delete_todo_string_id():
    response = client.delete("/todo/abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Input should be a valid integer" in response.text

@pytest.mark.asyncio
async def test_create_todo_with_description():
    response = client.post("/todo", json={"title": "Task with Description", "description": "New Description"})
    assert response.status_code == status.HTTP_201_CREATED
    assert "Added new todo with id" in response.json()["message"]
    assert response.json()["todo"]["description"] == "New Description"

@pytest.mark.asyncio
async def test_update_todo_only_description():
    response = client.post("/todo", json={"title": "Task to Update", "description": "Old Desc"})
    todo_id = response.json()["todo"]["id"]
    response = client.put(f"/todo/{todo_id}", json={"id": todo_id, "title": "Task to Update", "description": "New Desc"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["todo"]["description"] == "New Desc"

@pytest.mark.asyncio
async def test_update_todo_only_is_done():
    response = client.post("/todo", json={"title": "Task to Update"})
    todo_id = response.json()["todo"]["id"]
    response = client.put(f"/todo/{todo_id}", json={"id": todo_id, "title": "Task to Update", "is_done": True})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["todo"]["is_done"] is True

@pytest.mark.asyncio
async def test_create_todo_with_float_id():
    response = client.post("/todo", json={"id": 1.0, "title": "Invalid ID"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "ID must be 0 or None" in response.text

@pytest.mark.asyncio
async def test_update_todo_with_float_id():
    response = client.put(f"/todo/2.5", json={"id": 2.5, "title": "Invalid ID"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Input should be a valid integer" in response.text