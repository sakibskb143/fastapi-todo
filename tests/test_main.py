# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from src.main import api, todos


client = TestClient(api)

# ensure tests are isolated: clear todos before and after each test
@pytest.fixture(autouse=True)
def clear_todos():
    todos.clear()
    yield
    todos.clear()

def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"Message": "Hello World"}

def test_create_todo():
    r = client.post("/todo", json={
        "id": 1,
        "name": "Study",
        "des": "Prepare for exams"
    })
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert body[0]["name"] == "Study"

def test_get_todos():
    # create an item first
    client.post("/todo", json={"id": 1, "name": "Study", "des": "Prepare for exams"})
    r = client.get("/todo")
    assert r.status_code == 200
    j = r.json()
    assert isinstance(j, list)
    assert len(j) == 1

def test_update_todo():
    client.post("/todo", json={"id": 1, "name": "Study", "des": "Prepare for exams"})
    r = client.put("/todo/1", json={
        "id": 1,
        "name": "Study Updated",
        "des": "Prepare for math exams"
    })
    assert r.status_code == 200
    body = r.json()
    assert body[0]["name"] == "Study Updated"

def test_delete_todo():
    client.post("/todo", json={"id": 1, "name": "Study", "des": "Prepare for exams"})
    client.put("/todo/1", json={"id": 1, "name": "Study Updated", "des": "Prepare for math exams"})
    r = client.delete("/todo/1")
    assert r.status_code == 200
    # delete returns the deleted item
    assert r.json() == {
        "id": 1,
        "name": "Study Updated",
        "des": "Prepare for math exams"
    }
