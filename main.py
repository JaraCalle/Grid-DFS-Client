import argparse
from modules.views.commands import *

def main():
    parser = argparse.ArgumentParser(prog="gridfs", description="Cliente GridDFS")
    subparsers = parser.add_subparsers(dest="command")

    # put
    put_parser = subparsers.add_parser("put")
    put_parser.add_argument("file", type=str)
    put_parser.add_argument("--dir", type=str, default="/")

    # get
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("filename", type=str)
    get_parser.add_argument("output", type=str)
    get_parser.add_argument("--dir", type=str, default="/")

    # ls
    ls_parser = subparsers.add_parser("ls")
    ls_parser.add_argument("--dir", type=str, default="/")

    # rm
    rm_parser = subparsers.add_parser("rm")
    rm_parser.add_argument("filename", type=str)
    rm_parser.add_argument("--dir", type=str, default="/")

    # mkdir
    mkdir_parser = subparsers.add_parser("mkdir")
    mkdir_parser.add_argument("dirname", type=str)
    mkdir_parser.add_argument("--parent", type=str, default="/")

    # rmdir
    rmdir_parser = subparsers.add_parser("rmdir")
    rmdir_parser.add_argument("dirname", type=str)
    rmdir_parser.add_argument("--parent", type=str, default="/")

    # tree
    subparsers.add_parser("tree", help="Muestra el árbol de directorios y archivos")

    args = parser.parse_args()

    if args.command == "put":
        cmd_put(args.file, args.dir)
    elif args.command == "get":
        cmd_get(args.filename, args.output, args.dir)
    elif args.command == "ls":
        cmd_ls(args.dir)
    elif args.command == "rm":
        cmd_rm(args.filename, args.dir)
    elif args.command == "mkdir":
        cmd_mkdir(args.dirname, args.parent)
    elif args.command == "rmdir":
        cmd_rmdir(args.dirname, args.parent)
    elif args.command == "tree":
        cmd_tree()

if __name__ == "__main__":
    main()
