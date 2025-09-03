import requests
from core.config import settings

TOKEN = None

def get_token():
    global TOKEN
    if TOKEN:
        return TOKEN

    url = f"{settings.NAMENODE_URL}/auth/login"
    payload = {"username": settings.USERNAME, "password": settings.PASSWORD}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()

    TOKEN = resp.json()["access_token"]
    return TOKEN
