import argparse
from modules.views.commands import *

def main():
    parser = argparse.ArgumentParser(prog="gridfs", description="Cliente GridDFS")
    subparsers = parser.add_subparsers(dest="command")

    # put
    put_parser = subparsers.add_parser("put", help="Subir archivo al sistema")
    put_parser.add_argument("file", type=str, help="Ruta del archivo a subir")

    # get
    get_parser = subparsers.add_parser("get", help="Descargar archivo desde el sistema")
    get_parser.add_argument("filename", type=str, help="Nombre del archivo en GridDFS")
    get_parser.add_argument("output", type=str, help="ruta de salida local")

    # ls
    subparsers.add_parser("ls")

    # rm
    rm_parser = subparsers.add_parser("rm")
    rm_parser.add_argument("filename", type=str, help="Nombre del archivo en GridDFS")

    # mkdir
    mkdir_parser = subparsers.add_parser("mkdir")
    mkdir_parser.add_argument("dirname", type=str, help="Nombre del directorio a crear")

    # rmdir
    rmdir_parser = subparsers.add_parser("rmdir")
    rmdir_parser.add_argument("dirname", type=str)

    args = parser.parse_args()

    if args.command == "put":
        cmd_put(args.file)
    elif args.command == "get":
        cmd_get(args.filename, args.output)
    elif args.command == "ls":
        cmd_ls()
    elif args.command == "rm":
        cmd_rm(args.filename)
    elif args.command == "mkdir":
        cmd_mkdir(args.dirname)
    elif args.command == "rmdir":
        cmd_rmdir(args.dirname)

if __name__ == "__main__":
    main()
