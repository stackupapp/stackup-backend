# app/services/auth_service.py
from typing import Dict
# app/services/auth_service.py
from passlib.context import CryptContext

__all__ = ["hash_password", "verify_password"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# temporary in-memory user store (username -> password)
user_store: Dict[str, str] = {}

def signup_user(username: str, password: str) -> bool:
    if username in user_store:
        return False
    user_store[username] = password
    return True

def login_user(username: str, password: str) -> bool:
    return user_store.get(username) == password