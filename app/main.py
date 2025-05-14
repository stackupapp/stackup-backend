# app/main.py
from fastapi import FastAPI
from app.api import auth

app = FastAPI()

# Root health check route
@app.get("/")
def root():
    return {"message": "StackUp backend is running"}

# Register auth route
app.include_router(auth.router)