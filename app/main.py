from fastapi import FastAPI
from app.api import auth

app = FastAPI()

@app.get("/")
def root():
    return {"message": "StackUp backend is running"}

app.include_router(auth.router)