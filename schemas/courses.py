from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
from datetime import datetime

class CourseSerializer(BaseModel):
    id: str = Field(..., alias="_id")
    course_code: str
    course_name: str
    year: str
    group: int
    number: int
    IsActive: bool = False
    IsDelete: bool = False
    createDate: datetime = None
    updateDate: datetime = None

def course_serializer(course) -> CourseSerializer:
    course["_id"] = str(course["_id"]) 
    return CourseSerializer(**course)

def courses_serializers(courses) -> List[CourseSerializer]:
    return [course_serializer(course) for course in courses]
