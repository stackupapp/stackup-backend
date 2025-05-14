# app/main.py
from fastapi import FastAPI
from app.api.auth_routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "StackUp backend is running"}

app.include_router(router)