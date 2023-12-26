from pydantic import BaseModel

class Course(BaseModel):
    course_code: str
    course_name: str
    year: str
    group: int
    number: int
