import os
from core.config import settings
from utils.files import split_file
from services.namenode import allocate_file, get_metadata, list_files, remove_file, make_dir, remove_dir, get_tree
from services.datanode import upload_block, download_block, delete_block


def cmd_put(filepath: str, directory: str = "/"):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    print(f"[INFO] Subiendo archivo {filename} a {directory}")

    blocks = allocate_file(filename, filesize, settings.BLOCK_SIZE, directory)

    for i, chunk in split_file(filepath, settings.BLOCK_SIZE):
        block_info = blocks[i]
        block_id = block_info["block_id"]
        datanode_ip = block_info["datanode"]["ip"]
        datanode_port = block_info["datanode"]["grpc_port"]

        print(f"[INFO] Subiendo bloque {i} a {datanode_ip}:{datanode_port}")
        upload_block(datanode_ip, datanode_port, block_id, chunk)

    print("[OK] Archivo subido exitosamente")


def cmd_get(filename: str, output_path: str, directory: str = "/"):
    print(f"[INFO] Descargando {filename} desde {directory}")

    metadata = get_metadata(filename, directory)["blocks"]
    blocks = sorted(metadata, key=lambda b: b["index"])

    with open(output_path, "wb") as f:
        for block in blocks:
            block_id = block["block_id"]
            dn_ip = block["datanode"]["ip"]
            dn_port = block["datanode"]["grpc_port"]

            print(f"[INFO] Descargando {block_id} desde {dn_ip}:{dn_port}")
            data = download_block(dn_ip, dn_port, block_id)
            f.write(data)

    print(f"[OK] Archivo reconstruido en {output_path}")

def cmd_ls(directory: str = "/"):
    resp = list_files(directory)
    print("Directories:", resp["directories"])
    print("Files:", resp["files"])

def cmd_rm(filename: str, directory: str = "/"):
    resp = remove_file(filename, directory)
    for block in resp["deleted"]["blocks"]:
        block_id = block["block_id"]
        datanode_host = block["datanode"]["ip"]
        datanode_port = block["datanode"]["grpc_port"]
        
        try:
            msg = delete_block(datanode_host, datanode_port, block_id)
            print(f"[OK] {msg}")
        except Exception as e:
            print(f"[WARN] Could not delete block {block_id}: {e}")


def cmd_mkdir(dirname: str, parent: str = "/"):
    resp = make_dir(dirname, parent)
    print(resp)

def cmd_rmdir(dirname: str, parent: str = "/"):
    resp = remove_dir(dirname, parent)
    print(resp["msg"])

    for block in resp.get("deleted_blocks", []):
        dn_ip = block["datanode"]["ip"]
        dn_port = block["datanode"]["grpc_port"]
        block_id = block["block_id"]

        try:
            msg = delete_block(dn_ip, dn_port, block_id)
            print(f"[OK] Deleted block {block_id} from {dn_ip}:{dn_port} -> {msg}")
        except Exception as e:
            print(f"[WARN] Could not delete block {block_id} from {dn_ip}:{dn_port} -> {e}")

def _print_tree(node: dict, prefix: str = ""):
    # Archivos en el directorio actual
    for fname in node.get("files", {}):
        print(f"{prefix}├── {fname}")
    # Subdirectorios
    subdirs = node.get("subdirs", {})
    for i, (dname, dcontent) in enumerate(subdirs.items()):
        connector = "└── " if i == len(subdirs) - 1 else "├── "
        print(f"{prefix}{connector}{dname}/")
        # Prefijo para los hijos (indentación)
        new_prefix = prefix + ("    " if i == len(subdirs) - 1 else "│   ")
        _print_tree(dcontent, new_prefix)

def cmd_tree():
    tree = get_tree()
    if not tree:
        print("[EMPTY] No hay archivos ni directorios para este usuario.")
        return
    print("/")
    _print_tree(tree["/"])