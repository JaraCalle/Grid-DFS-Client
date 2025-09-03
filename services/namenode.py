import requests
from core.config import settings
from services.auth import get_token

def allocate_file(filename: str, filesize: int, block_size: int):
    url = f"{settings.NAMENODE_URL}/namenode/allocate"
    headers = {"Authorization": f"Bearer {get_token()}"}
    payload = {"filename": filename, "filesize": filesize, "block_size": block_size}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["blocks"]

def get_metadata(filename: str):
    url = f"{settings.NAMENODE_URL}/namenode/metadata/{filename}"
    headers = {"Authorization": f"Bearer {get_token()}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()