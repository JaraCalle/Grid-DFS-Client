import requests
from core.config import settings

def allocate_file(filename: str, filesize: int, block_size: int):
    url = f"{settings.NAMENODE_URL}/allocate"
    headers = {"Authorization": f"Bearer {settings.AUTH_TOKEN}"}
    payload = {"filename": filename, "filesize": filesize, "block_size": block_size}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["blocks"]