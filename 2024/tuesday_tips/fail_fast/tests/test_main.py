from fastapi.testclient import TestClient
from employee_portal.main import app

client = TestClient(app)

def test_successful_employee_update():
    data = {"name": "John Doe", "position": "Software Engineer", "salary": 50000.0}
    response = client.put(url="/employees/1", params=data)

    print(response.content)
    assert response.status_code == 200
    assert response.json() == {"message": "Employee with ID 1 updated successfully"}

def test_update_non_existing_employee():
    data = {"name": "John Doe", "position": "Software Engineer", "salary": 50000.0}
    response = client.put(url="/employees/999", params=data)

    assert response.status_code == 422
    assert response.json() == {"detail": "Employee not found"}

def test_invalid_update_missing_fields():
    data = {"position": "Manager", "salary": 50000.0}
    response = client.put(url="/employees/1", params=data)

    assert response.status_code == 422

# You can add more test cases as needed
