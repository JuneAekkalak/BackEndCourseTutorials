from fastapi import FastAPI
from routes.courses import course_route

app = FastAPI()

app.include_router(course_route, prefix="/api/course")