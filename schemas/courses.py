from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from typing import Optional


class CourseSerializer(BaseModel):
    id: str = Field(..., alias="_id")
    course_code: str
    course_name: str
    course_decript: str = None
    year: str
    group: int
    number: int
    IsActive: bool = True
    IsDelete: bool = False
    createDate: datetime = None
    updateDate: datetime = None

def course_serializer(course) -> CourseSerializer:
    if course is None:
        return None
    course["_id"] = str(course["_id"]) 
    return CourseSerializer(**course)

def courses_serializers(courses) -> List[CourseSerializer]:
    return [course_serializer(course) for course in courses]
