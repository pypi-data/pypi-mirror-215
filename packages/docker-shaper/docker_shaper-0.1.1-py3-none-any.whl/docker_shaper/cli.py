#!/usr/bin/env python3

"""Docker Shaper command line interface
"""

from argparse import ArgumentParser
from argparse import Namespace as Args
from pathlib import Path

from docker_shaper import server

def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")

    parser.set_defaults(func=lambda *_: parser.print_usage())
    subparsers = parser.add_subparsers(help="available commands", metavar="CMD")

    parser_run = subparsers.add_parser("serve")
    parser_run.set_defaults(func=fn_serve)

    return parser.parse_args()


def fn_serve(args: Args) -> None:
    """Entry point for event consistency check"""
    server.serve()


def main() -> int:
    """Entry point for everything else"""
    (args := parse_args()).func(args)
    return 0


if __name__ == "__main__":
    main()
