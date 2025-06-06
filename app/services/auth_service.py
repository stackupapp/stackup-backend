import json
import os
from app.utils.hashing import hash_password, verify_password

USERS_FILE = "app/storage/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def signup_user(email: str, password: str):
    users = load_users()
    if email in users:
        return False, "User already exists"
    users[email] = {"password": hash_password(password)}
    save_users(users)
    return True, "User created successfully"

def authenticate_user(email: str, password: str):
    users = load_users()
    if email not in users:
        return False
    return verify_password(password, users[email]["password"])