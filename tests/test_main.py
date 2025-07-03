"""Tests for main application endpoints"""

from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "text/html; charset=utf-8"
