"""
Basic API tests using TestClient
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Periodic Table API" in data["message"]

def test_health_endpoint(client):
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_elements_empty(client):
    """Test getting elements when database is empty"""
    response = client.get("/elements")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_nonexistent_element(client):
    """Test getting a non-existent element"""
    response = client.get("/elements/X")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

def test_create_element_unauthorized(client):
    """Test creating element without authentication"""
    data = {"symbol": "X", "name": "Test", "number": 1, "info": "Test"}
    response = client.post("/elements", json=data)
    assert response.status_code == 401
    data = response.json()
    assert "not authenticated" in data["detail"].lower()
