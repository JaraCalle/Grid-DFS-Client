import requests
from core.config import settings
from services.auth import get_token

def allocate_file(filename: str, filesize: int, block_size: int, directory: str = "/"):
    url = f"{settings.NAMENODE_URL}/namenode/allocate"
    headers = {"Authorization": f"Bearer {get_token()}"}
    payload = {
        "filename": filename, 
        "filesize": filesize, 
        "block_size": block_size,
        "owner": "admin",
        "directory": directory
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["blocks"]

def get_metadata(filename: str, directory: str = "/"):
    url = f"{settings.NAMENODE_URL}/namenode/metadata/{filename}?directory={directory}"
    headers = {"Authorization": f"Bearer {get_token()}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def list_files(directory: str = "/"):
    url = f"{settings.NAMENODE_URL}/namenode/ls?directory={directory}"
    headers = {"Authorization": f"Bearer {get_token()}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def remove_file(filename: str, directory: str = "/") -> dict:
    url = f"{settings.NAMENODE_URL}/namenode/rm/{filename}?directory={directory}"
    headers = {"Authorization": f"Bearer {get_token()}"}
    resp = requests.delete(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def make_dir(dirname: str, parent: str = "/"):
    url = f"{settings.NAMENODE_URL}/namenode/mkdir?dirname={dirname}&parent={parent}"
    headers = {"Authorization": f"Bearer {get_token()}"}
    resp = requests.post(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def remove_dir(dirname: str, parent: str = "/"):
    url = f"{settings.NAMENODE_URL}/namenode/rmdir?dirname={dirname}&parent={parent}"
    headers = {"Authorization": f"Bearer {get_token()}"}
    resp = requests.delete(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_tree():
    url = f"{settings.NAMENODE_URL}/namenode/tree"
    headers = {"Authorization": f"Bearer {get_token()}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()