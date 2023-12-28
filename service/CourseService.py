from fastapi import HTTPException
from config.database import course_collection  
from bson import ObjectId
from typing import Optional
from schemas.courses import courses_serializers, course_serializer
from models.courses import Course, SearchRequestModel
from datetime import datetime


async def Search(request: SearchRequestModel):
    query = build_query(request)
    courses = courses_serializers(course_collection.find(query))
    return courses

async def Read(id: str):
    course_doc = course_collection.find_one({"_id": ObjectId(id)})
    if course_doc:
        return course_serializer(course_doc)
    raise HTTPException(status_code=404, detail="Course not found")

async def Crate(course: Course):
    course_dict = dict(course)
    _id = course_collection.insert_one(course_dict)
    return courses_serializers(course_collection.find({"_id": _id.inserted_id}))

async def Update(id: str, course: Course):
    result = course_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(course)})
    if result:
        return courses_serializers(course_collection.find({"_id": ObjectId(id)}))
    raise HTTPException(status_code=404, detail="Course not found")

async def PatchAcitve(id: str, IsActive: bool):
    result = course_collection.update_one({"_id": ObjectId(id)}, {"$set": {"IsActive": IsActive, "updateDate": datetime.utcnow()}})
    if result.modified_count > 0:
        return course_collection.find_one({"_id": ObjectId(id)})
    raise HTTPException(status_code=404, detail="Course not found")

async def PatchDelete(id: str, IsDelete: bool):
    result = course_collection.update_one({"_id": ObjectId(id)}, {"$set": {"IsDelete": IsDelete, "updateDate": datetime.utcnow()}})
    if result.modified_count > 0:
        return course_collection.find_one({"_id": ObjectId(id)})
    raise HTTPException(status_code=404, detail="Course not found")

async def Delete(id: str):
    result = course_collection.find_one_and_delete({"_id": ObjectId(id)})
    if result:
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Course not found")

# Fuction
def build_query(request) -> dict:
    query = {}
    if request.course_code:
        query["course_code"] = request.course_code
    if request.course_name:
        query["course_name"] = request.course_name
    if request.year:
        query["year"] = request.year
    if request.IsActive is not None:
        query["IsActive"] = request.IsActive
    if request.IsDelete is not None:
        query["IsDelete"] = request.IsDelete
    return query


   
