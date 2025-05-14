# app/services/auth_service.py
from typing import Dict

# temporary in-memory user store (username -> password)
user_store: Dict[str, str] = {}

def signup_user(username: str, password: str) -> bool:
    if username in user_store:
        return False
    user_store[username] = password
    return True

def login_user(username: str, password: str) -> bool:
    return user_store.get(username) == password