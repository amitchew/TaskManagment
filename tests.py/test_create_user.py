import json
from fastapi.testclient import TestClient
from app.main import app
client= TestClient(app)
def test_create_task():
    test_task_data={
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2024-25-01",
        "status":"to do",
        "creator": "test_user"
    }

    response= client.pst("/tasks/", json= test_task_data)
    
    
    assert response.status_code == 200
    assert response.json()["title"]== test_task_data["title"]
    assert response.json()["description"]== test_task_data["description"]
    assert response.json()["due_date"]== test_task_data["due_date"]
    assert response.json()["status"]== test_task_data["status"]
    assert response.json()["creator"]== test_task_data["creator"]
