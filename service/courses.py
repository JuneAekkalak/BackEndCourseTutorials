from fastapi import HTTPException,status
from config.database import course_collection
from bson import ObjectId 
from bson.errors import InvalidId
from schemas.courses import courses_serializers, course_serializer
from models.courses import Course, SearchRequestModel
from datetime import datetime
import re


async def Search(request: SearchRequestModel):
    query = build_query(request)
    courses = courses_serializers(course_collection.find(query))
    return courses


async def Read(id: str):
    course = find_course_by_id(id)
    if course:
        return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


async def Create(course: Course):
    course_dict = create_course(course)
    
    unique_query = {
        "course_code": course_dict["course_code"],
        "year": course_dict["year"],
        "group": course_dict["group"]
    }
    
    existing_course = course_collection.find_one(unique_query)
    
    if existing_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate Course")
    
    _id = course_collection.insert_one(course_dict)
    
    return {
        "status": "success",
        "message": "Course create successfully",
        "_id": str(_id.inserted_id)
    }


async def Update(id: str, course: Course):
    result = course_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(course)}
    )
    if result:
        return {"status": "success", "message": "Course update successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


async def PatchActive(id: str, IsActive: bool):
    result = update_course_status(id, "IsActive", IsActive)
    if result:
        return {"status": "success", "message": "Course update successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


async def PatchDelete(id: str, IsDelete: bool):
    result = update_course_status(id, "IsDelete", IsDelete)
    if result:
        return {"status": "success", "message": "Course update successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


async def Delete(id: str):
    result = course_collection.find_one_and_delete({"_id": ObjectId(id)})
    if result:
        return {"status": "success", "message": "Course deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


#Tools
def build_query(request: SearchRequestModel) -> dict:
    query = {}
    if request.course_code:
        query["course_code"] = request.course_code
    if request.course_name:
        regex_pattern = re.compile(f".*{re.escape(request.course_name)}.*", re.IGNORECASE)
        query["course_name"] = regex_pattern
    if request.year:
        query["year"] = request.year
    if request.IsActive is not None:
        query["IsActive"] = request.IsActive
    if request.IsDelete is not None:
        query["IsDelete"] = request.IsDelete
    return query

def find_course_by_id(id: str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return None  
    course = course_collection.find_one({"_id": object_id})
    return course_serializer(course)

def update_course_status(id: str, field: str, value):
    result = course_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": {field: value, "updateDate": datetime.utcnow()}}
    )
    if result.modified_count > 0:
        return find_course_by_id(id)
    return None

def create_course(course: Course):
    course_dict = {
        "course_code": course.course_code,
        "course_name": course.course_name,
        "course_decript": course.course_decript,
        "year": course.year,
        "group": course.group,
        "number": course.number,
        "IsActive": True,  
        "IsDelete": False,  
        "createDate": datetime.utcnow(), 
        "updateDate": datetime.utcnow()  
    }
    return course_dict