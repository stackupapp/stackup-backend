# app/api/auth.py
from fastapi import APIRouter, HTTPException
from app.models.user import SignUpRequest, LoginRequest, AuthResponse
from app.services.auth_service import signup_user, login_user

router = APIRouter()

@router.post("/signup", response_model=AuthResponse)
def signup(payload: SignUpRequest):
    success = signup_user(payload.username, payload.password)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User signed up successfully"}

@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    success = login_user(payload.username, payload.password)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}