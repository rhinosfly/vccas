from argparse import Namespace
import hashlib

from .config import get_config


def get_file_checksum(file_name: str):
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()    
        checksum = hashlib.md5(data).hexdigest()
    return checksum

def verify(args: Namespace):
    config = get_config(args.CONFIG)
    ORIGINAL = config["archives"][0]
    NEW_FILE = config["documents"][0]

    original_md5 = get_file_checksum(ORIGINAL)
    new_file_md5 = get_file_checksum(NEW_FILE)
    print("original:\t",original_md5)
    print("new_file:\t",new_file_md5)

    if original_md5 == new_file_md5:
        print("MD5 verification:\nsuccess!")
    else:
        print("MD5 verification:\nfailed!")


def main():
    args = Namespace(CONFIG=".")
    verify(args)


if __name__ == "__main__":
    main()
