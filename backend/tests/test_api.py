from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert "version" in data
    assert data["status"] == "operational"

def test_cors_headers():
    """Test that CORS headers are set correctly."""
    response = client.options(
        "/",
        headers={"Origin": "http://localhost:5173"}
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173" 