from fastapi import APIRouter, HTTPException
from config.database import collection_name
from bson import ObjectId
from typing import List
from schemas.courses import courses_serializers, course_serializer, CourseSerializer
from models.courses import Course

course = APIRouter()

# Retrieve
@course.get("/", response_model=List[CourseSerializer])
async def get_courses():
    courses = courses_serializers(collection_name.find())
    return courses

@course.get("/{id}", response_model=CourseSerializer)
async def get_course(id: str):
    course = collection_name.find_one({"_id": ObjectId(id)})
    if course:
        return course_serializer(course)
    raise HTTPException(status_code=404, detail="Course not found")

# Create
@course.post("/", response_model=List[CourseSerializer])
async def create_course(course: Course):
    course_dict = dict(course)
    _id = collection_name.insert_one(course_dict)
    return courses_serializers(collection_name.find({"_id": _id.inserted_id}))

# Update
@course.put("/{id}", response_model=List[CourseSerializer])
async def update_course(id: str, course: Course):
    result = collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(course)})
    if result:
        return courses_serializers(collection_name.find({"_id": ObjectId(id)}))
    raise HTTPException(status_code=404, detail="Course not found")

# Delete
@course.delete("/{id}")
async def delete_course(id: str):
    result = collection_name.find_one_and_delete({"_id": ObjectId(id)})
    if result:
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Course not found")


