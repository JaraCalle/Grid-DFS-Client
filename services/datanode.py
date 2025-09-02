import requests

def upload_block(datanode_info: str, block_id: str, data: bytes):
    """
    datanode_info llega como 'dn1' (id) pero en la práctica deberíamos 
    resolver ip:port desde el NameNode.
    Supongamos que el NameNode devuelve directamente 'http://ip:port'.
    """
    url = f"{datanode_info}/api/v1/block/{block_id}"
    files = {"file": (block_id, data)}
    resp = requests.put(url, files=files)
    resp.raise_for_status()
    return resp.json()
