from fastapi import FastAPI
from routes.courses import course

app = FastAPI()

app.include_router(course)