import pytest
from unittest.mock import MagicMock
from service.courses import build_query, find_course_by_id
from bson import ObjectId
from schemas.courses import course_serializer

# Start test build_query function   
@pytest.mark.asyncio
async def test_build_query_only_course_code():
    mock_request = MagicMock()
    mock_request.course_code = "CS101"
    
    mock_request.course_name = None
    mock_request.year = None
    mock_request.IsActive = None
    mock_request.IsDelete = None
    
    query = build_query(mock_request)
    assert query == {"course_code": "CS101"}

@pytest.mark.asyncio
async def test_build_query_course_code_and_name():
    mock_request = MagicMock()
    mock_request.course_code = "CS101"
    mock_request.course_name = "Introduction to CS"
    
    mock_request.year = None
    mock_request.IsActive = None
    mock_request.IsDelete = None
    
    query = build_query(mock_request)
    assert query == {"course_code": "CS101", "course_name": "Introduction to CS"}

@pytest.mark.asyncio
async def test_build_query_all_attributes():
    mock_request = MagicMock()
    mock_request.course_code = "CS101"
    mock_request.course_name = "Introduction to CS"
    mock_request.year = 2023
    
    mock_request.IsActive = None
    mock_request.IsDelete = None
    
    query = build_query(mock_request)
    assert query == {"course_code": "CS101", "course_name": "Introduction to CS", "year": 2023}

@pytest.mark.asyncio
async def test_build_query_is_active():
    mock_request = MagicMock()
    mock_request.IsActive = True
    
    mock_request.course_code = None
    mock_request.course_name = None
    mock_request.year = None
    mock_request.IsDelete = None
     
    query = build_query(mock_request)
    assert query == {"IsActive": True}

@pytest.mark.asyncio
async def test_build_query_is_delete():
    mock_request = MagicMock()
    mock_request.IsDelete = False
    
    mock_request.course_code = None
    mock_request.course_name = None
    mock_request.year = None
    mock_request.IsActive = None
    
    query = build_query(mock_request)
    assert query == {"IsDelete": False}


@pytest.mark.asyncio
async def test_build_query_multiple_attributes():
    mock_request = MagicMock()
    mock_request.course_code = "CS101"
    mock_request.course_name = "Introduction to CS"
    mock_request.year = 2023
    mock_request.IsActive = True
    mock_request.IsDelete = False
    
    query = build_query(mock_request)
    assert query == {
        "course_code": "CS101",
        "course_name": "Introduction to CS",
        "year": 2023,
        "IsActive": True,
        "IsDelete": False
    }

# End test build_query function   

# Start test find_course_by_id function
@pytest.fixture
def mock_course_collection(monkeypatch):
    mock_collection = MagicMock()
    monkeypatch.setattr('config.database.course_collection', mock_collection)
    return mock_collection

def test_find_course_by_id_with_valid_id(mock_course_collection, monkeypatch): 
    result = mock_course_collection.find_one.return_value = {
        "_id": "658ec84ac50761120f7356a4",  
        "course_code": "123", 
        "course_name": "Test Course",
        "course_decript": "string",
        "year": "2023", 
        "group": 10,  
        "number": 20,
        "IsActive": True,
        "IsDelete": False,
        "createDate": "2023-12-29T13:22:38.166000",
        "updateDate": "2023-12-30T03:51:00.798000"
    }
    
    monkeypatch.setattr('schemas.courses.course_serializer', lambda x: course_serializer(x))
    
    expected_result = {
        "_id": "658ec84ac50761120f7356a4",  
        "course_code": "123", 
        "course_name": "Test Course",
        "course_decript": "string",
        "year": "2023", 
        "group": 10,  
        "number": 20,
        "IsActive": True,
        "IsDelete": False,
        "createDate": "2023-12-29T13:22:38.166000",
        "updateDate": "2023-12-30T03:51:00.798000"
    }
    
    assert result == expected_result
   
def test_find_course_by_id_with_invalid_id(mock_course_collection, monkeypatch): 
    mock_course_collection.find_one.return_value = None
    
    monkeypatch.setattr('schemas.courses.course_serializer', lambda x: {"course_name": x["name"]})
    
    result = find_course_by_id("invalid_id")
    assert result is None

# End test find_course_by_id function



