from fastapi.testclient import TestClient
import sys

sys.path.insert(0, "../05.2Lab")
from main import app

client = TestClient(app)
course_id = None

def test_create_course():
    payload = {
        "course_code": "C353",
        "course_name": "Course Create",
        "year": "3",
        "group": 1,
        "number": 30
    }
    response = client.post("/", json=payload)
    assert response.status_code == 200
    global course_id
    course_id = response.json()[0]['id']
    assert response.json()[0]['course_code'] == "C353"

def test_get_courses():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_retrieve_course_by_id():
    response = client.get(f"/{course_id}")
    assert response.status_code == 200
    assert response.json()['id'] == course_id
    assert response.json()["course_code"] == "C353"
    assert isinstance(response.json(), dict)

def test_update_course():
    updated_payload = {
        "course_code": "C354",
        "course_name": "Course Updated",
        "year": "3",
        "group": 2,
        "number": 30
    }
    response = client.put(f"/{course_id}", json=updated_payload)
    assert response.status_code == 200
    assert response.json()[0]['id'] == course_id
    assert response.json()[0]["course_code"] == "C354"
    assert isinstance(response.json(), list)

def test_delete_course():
    response = client.delete(f"/{course_id}")
    assert response.status_code == 200
    assert response.json()['status'] == "ok"
