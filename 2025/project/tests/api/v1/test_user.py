from fastapi.testclient import TestClient

from app.api.v1.user import get_user_service
from app.main import app
from app.services.user_service import UserService
from tests.test_db import TestingSessionLocal

# Setup the TestClient
client = TestClient(app)


# Dependency to override the get_db dependency in the main app
def override_get_user_service():
    session = TestingSessionLocal()
    yield UserService(session=session)


app.dependency_overrides[get_user_service] = override_get_user_service


def test_create_and_get_user():
    # Create a new user
    response = client.post("/api/v1/users", json={"name": "Test User"})
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["name"] == "Test User"
    assert "id" in created_user

    # Fetch the same user
    get_response = client.get(f"/api/v1/users/{created_user['id']}")
    assert get_response.status_code == 200
    fetched_user = get_response.json()
    assert fetched_user["id"] == created_user["id"]
    assert fetched_user["name"] == "Test User"
