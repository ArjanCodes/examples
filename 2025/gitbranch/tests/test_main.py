from fastapi.testclient import TestClient
from src.main import app

# Setup the TestClient
client = TestClient(app)


def test_hello():
    response = client.get("/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Hello, World!"


def test_hello_name():
    response = client.get("/?name=Test")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Hello, Test!"


def test_goodbye():
    response = client.get("/goodbye")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Goodbye, World!"


def test_goodbye_name():
    response = client.get("/goodbye?name=Test")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Goodbye, Test!"


def test_hello_formal():
    response = client.get("/?formal=True")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Good day to you, World."
