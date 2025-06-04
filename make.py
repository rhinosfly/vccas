'''extract zip archive into docx'''
import shutil
from os.path import relpath
from typing import Any
import pandoc
import sys
from config import get_config

def convert(src: str, dst: str):
    tmp = pandoc.read(file=src)
    pandoc.write(tmp, file=dst)

def make_docx(config: dict[str,Any]):
    '''create docx from xml'''
    for i,_ in enumerate(config["documents"]):
        target = config["targets"][i]
        archive = config["archives"][i]
        doc = config["documents"][i]
        # make zip
        print(f"archive \t{relpath(target)} \tto \t{relpath(archive)}")
        shutil.make_archive(base_name=archive, root_dir=target, format="zip")
        # copy to docx
        print(f"copy \t{relpath(archive)} \tto \t{relpath(doc)}")
        shutil.copy2(src=archive, dst=doc)

def make_xml(config: dict[str,Any]):
    '''extract xml from docx'''
    for i in range(len(config["documents"])):
        doc = config["documents"][i]
        archive = config["archives"][i]
        target = config["targets"][i]
        markdown = target + ".md"

        print(f"copy \t{relpath(doc)} \tto \t{relpath(archive)}")
        shutil.copy2(src=doc, dst=archive)
        
        print(f"unpack \t{relpath(archive)} \tto \t{relpath(target)}")
        shutil.unpack_archive(filename=archive, extract_dir=target)

        print(f"convert \t{relpath(doc)} \tto \t{relpath(markdown)}")
        convert(src=doc, dst=markdown)




def main(config: dict[str,Any]):
    if len(sys.argv) != 2:
        raise BaseException("not enough arguments")
    if sys.argv[1] == "docx":
        make_docx(config)
    if sys.argv[1] == "xml":
        make_xml(config)
    else:
        raise BaseException("invalid subcommand")
    

if __name__ == "__main__":
    config = get_config()
    main(config)