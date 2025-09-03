import argparse
from modules.views.commands import cmd_put, cmd_get

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

    args = parser.parse_args()

    if args.command == "put":
        cmd_put(args.file)
    elif args.command == "get":
        cmd_get(args.filename, args.output)

if __name__ == "__main__":
    main()
