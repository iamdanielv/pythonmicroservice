"""Tests for todos endpoint and status endpoints

This module contains unit tests for the todos endpoint and status endpoints
 in our RESTful API. It covers:
- Basic endpoint validation for /status and /
- Todo retrieval (GET /todos)
- Todo creation with parameter validation (POST /todo)
- Todo retrieval and update with ID validation (GET/PUT /todo/{id})
- Error handling for invalid payloads and IDs
- Status code and response message verification for endpoints
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "endpoint, method, payload, expected_status, expected_message",
    [
        ("/status", "GET", None, status.HTTP_200_OK, "OK"),
    ],
)
def test_endpoints(
    endpoint, method, payload, expected_status, expected_message
):
    response = client.request(method, endpoint, json=payload)
    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message


@pytest.mark.asyncio
async def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "todos" in data
    assert isinstance(data["todos"], list)


@pytest.mark.parametrize(
    "payload, expected_status, expected_message",
    [
        (
            {"title": "New Task"},
            status.HTTP_201_CREATED,
            "Added new todo with id",
        ),
        (
            {"id": 1, "title": "Invalid ID 1"},
            status.HTTP_400_BAD_REQUEST,
            "ID must be 0 or None",
        ),
        (
            {"id": -1, "title": "Invalid ID -1"},
            status.HTTP_400_BAD_REQUEST,
            "ID must be 0 or None",
        ),
        (
            {"id": "invalid", "title": "Invalid ID invalid"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid integer",
        ),
        (
            {"id": 1.0, "title": "Invalid ID 1.0"},
            status.HTTP_400_BAD_REQUEST,
            "ID must be 0 or None",
        ),
        (
            {"id": 1.5, "title": "Invalid ID 1.5"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid integer",
        ),
        (
            {"id": -1.5, "title": "Invalid ID -1.5"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid integer",
        ),
        (
            {"id": 0, "title": "Valid"},
            status.HTTP_201_CREATED,
            "Added new todo with id",
        ),
        (
            {"id": None, "title": "Valid"},
            status.HTTP_201_CREATED,
            "Added new todo with id",
        ),
    ],
)
def test_create_todo(payload, expected_status, expected_message):
    response = client.post("/todo", json=payload)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_201_CREATED:
        assert expected_message in response.json()["message"]
    else:
        assert expected_message in response.text


@pytest.mark.parametrize(
    "todo_id, expected_status, expected_message, fuzzy_match",
    [
        (1, status.HTTP_200_OK, "OK", False),
        (999, status.HTTP_404_NOT_FOUND, "Todo 999 not found", False),
        (0, status.HTTP_400_BAD_REQUEST, "ID must be a positive integer", True),
        (
            "abc",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid integer",
            True,
        ),
        (
            1.5,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid integer",
            True,
        ),
        (
            -1,
            status.HTTP_400_BAD_REQUEST,
            "ID must be a positive integer",
            True,
        ),
    ],
)
def test_get_todo(todo_id, expected_status, expected_message, fuzzy_match):
    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == expected_status
    if fuzzy_match:
        assert expected_message in response.text
    else:
        if expected_status == status.HTTP_404_NOT_FOUND:
            assert expected_message in response.text
        else:
            if expected_status == status.HTTP_422_UNPROCESSABLE_ENTITY:
                assert expected_message in response.json()["detail"]
            else:
                assert response.json()["message"] == expected_message


@pytest.mark.parametrize(
    "todo_id, payload, expected_status, expected_message",
    [
        (
            1,
            {"title": "Updated Task"},
            status.HTTP_200_OK,
            "OK, updated Todo 1",
        ),
        (
            1,
            {"id": 2, "title": "URL and body ID mismatch"},
            status.HTTP_400_BAD_REQUEST,
            "Todo id from URL: 1 does not match body id: 2",
        ),
        (
            1,
            {"id": "abc", "title": "Invalid ID abc"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid integer",
        ),
        (
            1.5,
            {"id": "1.5", "title": "Invalid ID 1.5"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid integer",
        ),
        (
            1,
            {"id": "1", "description": "New Desc, missing title"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Field required",
        ),
        (
            1,
            {"id": "1", "title": "invalid description", "description": 123},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid string",
        ),
    ],
)
def test_update_todo(todo_id, payload, expected_status, expected_message):
    response = client.put(f"/todo/{todo_id}", json=payload)
    assert response.status_code == expected_status
    assert expected_message in response.text


@pytest.mark.parametrize(
    "payload, expected_status, expected_message",
    [
        (
            {"title": "Updated Task", "description": "New Description"},
            status.HTTP_200_OK,
            "OK, updated Todo",
        ),
        (
            {"description": "New Desc"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Field required",
        ),
        (
            {"is_done": True},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Field required",
        ),
        (
            {"title": "Todo with Description", "is_done": True},
            status.HTTP_200_OK,
            "OK, updated Todo",
        ),
        (
            {"is_done": "makeit"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Field required",
        ),
        (
            {"title": "Todo with Description", "is_done": "makeit"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input should be a valid boolean",
        ),
    ],
)
def test_create_and_update_todo(payload, expected_status, expected_message):
    # Create a new todo to update
    response = client.post("/todo", json={"title": "Todo with Description"})
    assert response.status_code == status.HTTP_201_CREATED
    todo_id = response.json()["todo"]["id"]

    # Prepare the payload with the todo ID
    update_payload = {**payload, "id": todo_id}

    # Perform the update
    response = client.put(f"/todo/{todo_id}", json=update_payload)
    assert response.status_code == expected_status
    assert expected_message in response.text
