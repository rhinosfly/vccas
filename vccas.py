'''root of application'''

import argparse
import size
import verify
import convert

PROGRAM_NAME = "vccas"
VERSION = "v0.1.1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=f"{PROGRAM_NAME} {VERSION}" )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("CONFIG", help="config file path, or directory to search", default=".", nargs="?")

    subparsers = parser.add_subparsers(title="subcommands", required = True)
    extracter = subparsers.add_parser("extract", help="extract source to target", parents=[parent_parser])
    extracter.set_defaults(func=convert.extract)
    archiver = subparsers.add_parser("archive", help="archive target to source", parents=[parent_parser])
    archiver.set_defaults(func=convert.archive)
    verifier  = subparsers.add_parser('verify', help="verify source matches archive", parents=[parent_parser])
    verifier.set_defaults(func=verify.verify)
    measure = subparsers.add_parser("measure", help="record and print size of configured files", parents=[parent_parser])
    measure.set_defaults(func=size.measure)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()    
