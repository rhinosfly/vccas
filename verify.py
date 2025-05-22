import hashlib
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
NAME = "RSR00114_Rev. 3 (Test Report, TCD, AC Power Testing)"
ORIGINAL = DIR_PATH + "/../target/" + NAME + ".zip"
NEW_FILE = DIR_PATH + "/../src/" + NAME + ".docx"

def get_file_checksum(file_name):
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()    
        checksum = hashlib.md5(data).hexdigest()
    return checksum

def main():
    original_md5 = get_file_checksum(ORIGINAL)
    new_file_md5 = get_file_checksum(NEW_FILE)
    print("original:\t",original_md5)
    print("new_file:\t",new_file_md5)

    if original_md5 == new_file_md5:
        print("MD5 verification:\nsuccess!")
    else:
        print("MD5 verification:\nfailed!")


main()
