from fastapi import APIRouter, Depends
from service import CourseService
from typing import List
from schemas.courses import CourseSerializer
from models.courses import Course, SearchRequestModel

course_route = APIRouter()

# Retrieve
@course_route.get("/", response_model=List[CourseSerializer])
async def Search(request: SearchRequestModel = Depends()):
    return await CourseService.Search(request)

@course_route.get("/{id}", response_model=CourseSerializer)
async def Read(id: str):
   return await CourseService.Read(id)

# Create
@course_route.post("/", response_model=List[CourseSerializer])
async def Create(course: Course):
    return await CourseService.Create(course)

# Update
@course_route.put("/{id}", response_model=List[CourseSerializer])
async def Update(id: str, course: Course):
    return await CourseService.Update(id, course)

# PatchActive
@course_route.patch("/{id}/active", response_model=Course)
async def PatchActive(id: str, IsActive: bool):
   return await CourseService.PatchAcitve(id, IsActive)

# PatchDelete
@course_route.patch("/{id}/delete", response_model=Course)
async def PatchDelete(id: str, IsDelete: bool):
    return await CourseService.PatchDelete(id, IsDelete)

# Delete
@course_route.delete("/{id}")
async def Delete(id: str):
    return await CourseService.Delete(id)
