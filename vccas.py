'''root of application'''

import argparse
import size
import verify
import convert

PROGRAM_NAME = "vccas"
VERSION = "v0.2.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=f"{PROGRAM_NAME} {VERSION}" )

    subparsers = parser.add_subparsers(title="subcommands", required = True)
    extracter = subparsers.add_parser("extract", help="extract source to target")
    extracter.set_defaults(func=convert.make_xml)
    archiver = subparsers.add_parser("archive", help="archive target to source")
    archiver.set_defaults(func=convert.make_docx)
    verifier  = subparsers.add_parser('verify', help="verify source matches archive")
    verifier.set_defaults(func=verify.main)
    measure = subparsers.add_parser("measure", help="measure size configured files")
    measure.set_defaults(func=size.main)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    args.func()


if __name__ == "__main__":
    main()    
