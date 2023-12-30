from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Course(BaseModel):
    course_code: str
    course_name: str
    course_decript: str = None
    year: str
    group: int
    number: int

class CourseUpdateRequestModel(BaseModel):
    course_code: str
    course_name: str
    course_decript: str = None
    year: str
    group: int
    number: int

class SearchRequestModel(BaseModel):
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    year: Optional[str] = None
    IsActive: Optional[bool] = None
    IsDelete: Optional[bool] = None