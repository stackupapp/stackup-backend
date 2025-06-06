from fastapi import APIRouter, HTTPException
from app.models.user import UserSignup, UserLogin, TokenResponse
from app.services.auth_service import signup_user, authenticate_user
from app.utils.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: UserSignup):
    success, message = signup_user(user.email, user.password)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"msg": message}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    if not authenticate_user(user.email, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token}