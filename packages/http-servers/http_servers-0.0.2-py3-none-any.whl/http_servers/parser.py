import argparse
import sys
from typing import List

from http_servers.options import ServerOptions


def build_parser():
    parser = argparse.ArgumentParser(
        add_help=False, description="Run HTTP server in given folder"
    )
    parser.add_argument(
        "--cors", action="store_true", help="Pass this flag to enable cors"
    )
    parser.add_argument(
        "-h",
        "--host",
        default="localhost",
        type=str,
        help="Address on which server will listen",
    )
    parser.add_argument(
        "-p", "--port", default=7000, type=int, help="Port on which server will listen"
    )
    parser.add_argument("-d", "--source-dir", default=".")
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Watch changes in directory and invalidate cache on change.",
    )
    parser.add_argument("--help", action="store_true", help="Show this help")
    return parser


def parse_options(args: List[str] = None):
    parser = build_parser()
    namespace = parser.parse_args(args)
    raw_options = vars(namespace)

    display_help = raw_options.pop("help")
    if display_help:
        parser.print_help()
        sys.exit(0)

    return ServerOptions(**raw_options)
