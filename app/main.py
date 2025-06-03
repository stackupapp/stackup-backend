# app/main.py
import sys
import os

# Ensures that "core.config" resolves correctly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.api.auth_routes import router as auth_router
from core.config import settings

app = FastAPI()

@app.get("/")
def root():
    return {"message": "StackUp backend is running"}

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth")