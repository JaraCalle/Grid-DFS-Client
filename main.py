import argparse
import os
from core.config import settings
from utils.files import split_file
from services.namenode import allocate_file
from services.datanode import upload_block

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
        datanode = block_info["datanode"]

        print(f"[INFO] Subiendo bloque {i} a {datanode}")
        upload_block(datanode, block_id, chunk)

    print("[OK] Archivo subido exitosamente")

def main():
    parser = argparse.ArgumentParser(prog="gridfs", description="Cliente GridDFS")
    subparsers = parser.add_subparsers(dest="command")

    put_parser = subparsers.add_parser("put", help="Subir archivo al sistema")
    put_parser.add_argument("file", type=str, help="Ruta del archivo a subir")

    args = parser.parse_args()

    if args.command == "put":
        cmd_put(args.file)

if __name__ == "__main__":
    main()
