# app/main.py
from fastapi import FastAPI
from app.api.auth_routes import router as auth_router
from core.config import settings

app = FastAPI()

@app.get("/")
def root():
    return {"message": "StackUp backend is running"}

app.include_router(auth_router, prefix="/auth")

