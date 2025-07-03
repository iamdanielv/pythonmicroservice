"""Tests for the data models"""

import pytest
from pydantic import ValidationError

from src.models import Todo


def test_todo_model():
    """Test the Todo model"""
    # Test with valid data
    todo = Todo(id=1, title="Test", description="Test description", is_done=False)
    assert todo.id == 1
    assert todo.title == "Test"
    assert todo.description == "Test description"
    assert todo.is_done is False

    # Test with invalid data
    with pytest.raises(ValidationError):
        Todo(id=-1, title="Test", description="Test description", is_done=False)
