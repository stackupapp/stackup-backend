# app/services/auth_service.py
from typing import Dict
# app/services/auth_service.py
from passlib.context import CryptContext

# In-memory store (temporary)
user_db = {}

__all__ = ["hash_password", "verify_password"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# temporary in-memory user store (username -> password)
user_store: Dict[str, str] = {}

def signup_user(username: str, password: str) -> bool:
    if username in user_db:
        return False
    hashed_password = pwd_context.hash(password)
    user_db[username] = hashed_password
    return True

def login_user(username: str, password: str) -> bool:
    if username not in user_db:
        return False
    return pwd_context.verify(password, user_db[username])