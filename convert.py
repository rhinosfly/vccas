'''extract zip archive into docx'''
from argparse import Namespace
import shutil
from os import path
from os.path import relpath
from typing import Callable
import pandoc
import pandas
import sys
from config import get_config

class Conversion_Target:
    def __init__(self, target_type: str, converter: Callable[[str, str], None]):
        self.target_type = target_type
        self.convert = converter

def convert_pandoc(src: str, dst: str):
    tmp = pandoc.read(file=src)
    pandoc.write(tmp, file=dst)

def excel_to_csv(excel: str, csv: str):
    data = pandas.read_excel(excel)
    data.to_csv(csv)

conversion_mappings = {
    "docx": Conversion_Target("markdown", convert_pandoc),
    "xlsx": Conversion_Target("csv", excel_to_csv),
    "other": Conversion_Target("markdown", convert_pandoc)
}
file_extention_mappings = {
    "markdown": "md"
}

def convert(src: str, dst: str):
    """call appropriate conversion function on files accoridng to conversion mappings"""
    src_type = path.splitext(src)[1]
    if src_type in conversion_mappings.keys():
        conversion_mappings[src_type].convert(src, dst)
    else:
        conversion_mappings["other"].convert(src, dst)

def get_plaintext_file_extention(src: str) -> str:
    '''return corrosponding plaintext type for each archive type'''
    src_type = path.splitext(src)[1]
    if src_type in conversion_mappings.keys():
        target_type = conversion_mappings[src_type].target_type
    else:
        target_type = conversion_mappings["other"].target_type
    if target_type in file_extention_mappings.keys():
        file_extention = file_extention_mappings[target_type]
    else:
        file_extention = target_type
    return file_extention

def archive(args: Namespace):
    '''create document from xml'''
    config = get_config(args.CONFIG)
    for i,_ in enumerate(config["documents"]):
        target = config["targets"][i]
        archive = config["archives"][i]
        doc = config["documents"][i]
        # make zip
        print(f"archive \t{relpath(target)} \tto \t{relpath(archive)}")
        shutil.make_archive(base_name=archive, root_dir=target, format="zip")
        # copy to docx
        print(f"copy \t\t{relpath(archive)} \tto \t{relpath(doc)}")
        shutil.copy2(src=archive, dst=doc)

def extract(args: Namespace):
    '''extract xml from archive'''
    config = get_config(args.CONFIG)
    for i in range(len(config["documents"])):
        doc = config["documents"][i]
        archive = config["archives"][i]
        target = config["targets"][i]
        plaintext = target + "." + get_plaintext_file_extention(src=archive)

        print(f"copy \t\t{relpath(doc)} \tto \t{relpath(archive)}")
        shutil.copy2(src=doc, dst=archive)
        
        print(f"unpack \t\t{relpath(archive)} \tto \t{relpath(target)}")
        shutil.unpack_archive(filename=archive, extract_dir=target)

        print(f"convert \t{relpath(doc)} \tto \t{relpath(plaintext)}")
        convert(src=doc, dst=plaintext)




def main():
    args = Namespace(CONFIG=".")
    if len(sys.argv) != 2:
        raise BaseException("not enough arguments")
    if sys.argv[1] == "archive":
        archive(args)
    elif sys.argv[1] == "extract":
        extract(args)
    else:
        raise BaseException("invalid subcommand")
    

if __name__ == "__main__":
    main()