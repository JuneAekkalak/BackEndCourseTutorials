from fastapi import APIRouter, Depends
from service.courses import Search, Read, Create, Update, PatchActive, PatchDelete, Delete
from typing import List
from schemas.courses import CourseSerializer
from models.courses import Course, SearchRequestModel,CourseUpdateRequestModel

course_route = APIRouter(tags=["Courses"])

# Retrieve
@course_route.get("/", response_model=List[CourseSerializer])
async def CourseSearch(request: SearchRequestModel = Depends()):
    return await Search(request)

@course_route.get("/{id}", response_model=CourseSerializer)
async def CourseRead(id: str):
   return await Read(id)

# Create
@course_route.post("/")
async def CourseCreate(course: Course):
    return await Create(course)

# Update
@course_route.put("/{id}")
async def CourseUpdate(id: str, course: CourseUpdateRequestModel):
    return await Update(id, course)

# PatchActive
@course_route.patch("/{id}/active")
async def CoursePatchActive(id: str, IsActive: bool):
   return await PatchActive(id, IsActive)

# PatchDelete
@course_route.patch("/{id}/delete")
async def CoursePatchDelete(id: str, IsDelete: bool):
    return await PatchDelete(id, IsDelete)

# Delete
@course_route.delete("/{id}")
async def CourseDelete(id: str):
    return await Delete(id)
