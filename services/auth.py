import requests
import os
from core.config import settings

TOKEN_FILE = ".gridfs_token"
USER_FILE = ".gridfs_user"

def get_owner():
    if not os.path.exists(USER_FILE):
        raise Exception("No active user. Please login first.")
    with open(USER_FILE, "r") as f:
        return f.read().strip()

def register_user(username: str, password: str):
    url = f"{settings.NAMENODE_URL}/auth/register"
    payload = {"username": username, "password": password}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

def login_user(username: str, password: str):
    url = f"{settings.NAMENODE_URL}/auth/login"
    payload = {"username": username, "password": password}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    token = resp.json()["access_token"]

    # Guardar token
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    
    # Guardar username como "owner"
    with open(USER_FILE, "w") as f:
        f.write(username)

    return {"msg": "Login successful", "token": token}

def get_token():
    if not os.path.exists(TOKEN_FILE):
        raise Exception("You are not logged in. Please run: gridfs login <username> <password>")
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()

def logout_user():
    if os.path.exists(USER_FILE):
        os.remove(USER_FILE)
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        return {"msg": "Logged out successfully"}
    return {"msg": "No active session"}
