import pytest
from httpx import AsyncClient
from main import app

course_id = None

@pytest.fixture
def client():
    return AsyncClient(app=app, base_url="http://127.0.0.1:8000/")

@pytest.mark.asyncio
async def test_create_course(client):
    global course_id 
    course_data = {
        "course_code": "CSE101",
        "course_name": "Introduction to Computer Science",
        "year": "2023",
        "group": 1,
        "number": 101
    }
    response = await client.post("/api/courses/", json=course_data)
    assert response.status_code == 200
    course_id = str(response.json()["_id"])
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Course create successfully"

@pytest.mark.asyncio
async def test_get_course_by_id(client):
    global course_id 
    response = await client.get(f"/api/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["course_code"] == "CSE101"
    
@pytest.mark.asyncio
async def test_update_course(client):
    global course_id
    update_data = {
        "course_code": "CSE102",
        "course_name": "Advanced Computer Science",
        "year": "2024",
        "group": 2,
        "number": 102
    }
    response = await client.put(f"/api/courses/{course_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Course update successfully"

@pytest.mark.asyncio
async def test_patch_active_course(client):
    global course_id
    response = await client.patch(f"/api/courses/{course_id}/active?IsActive={True}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Course update successfully"

@pytest.mark.asyncio
async def test_patch_delete_course(client):
    global course_id
    response = await client.patch(f"/api/courses/{course_id}/delete?IsDelete={True}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Course update successfully"

@pytest.mark.asyncio
async def test_delete_course(client):
    global course_id
    response = await client.delete(f"/api/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Course deleted successfully"


