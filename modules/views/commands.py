import os
from core.config import settings
from utils.files import split_file
from services.namenode import allocate_file, get_metadata
from services.datanode import upload_block, download_block


def cmd_put(filepath: str):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    print(f"[INFO] Subiendo archivo {filename} ({filesize} bytes)")

    # 1. Pedir allocation al NameNode
    blocks = allocate_file(filename, filesize, settings.BLOCK_SIZE)

    # 2. Dividir archivo y subir cada bloque
    for i, chunk in split_file(filepath, settings.BLOCK_SIZE):
        block_info = blocks[i]
        block_id = block_info["block_id"]
        datanode_ip = block_info["ip"]
        datanode_port = block_info["port"]

        print(f"[INFO] Subiendo bloque {i} a {datanode_ip}:{datanode_port} vía gRPC")
        upload_block(datanode_ip, datanode_port, block_id, chunk)

    print("[OK] Archivo subido exitosamente")

def cmd_get(filename: str, output_path: str):
    print(f"[INFO] Descargando archivo {filename}")

    # 1. Obtener metadata desde NameNode
    metadata = get_metadata(filename)
    blocks = sorted(metadata, key=lambda b: b["index"])

    with open(output_path, "wb") as f:
        for block in blocks:
            block_id = block["block_id"]
            datanode_ip = block["ip"]
            datanode_port = block["port"]

            print(f"[INFO] Descargando bloque {block_id} desde {datanode_ip}:{datanode_port}")
            data = download_block(datanode_ip, datanode_port, block_id)
            f.write(data)

    print(f"[OK] Archivo reconstruido en {output_path}")
