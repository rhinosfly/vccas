'''extract zip archive into docx'''
import shutil
from os.path import relpath
from typing import Any
import pandoc
from config import get_config

def convert(src: str, dst: str):
    tmp = pandoc.read(file=src)
    pandoc.write(tmp, file=dst)


def main(config: dict[str,Any]):
    for i in range(len(config["documents"])):
        doc = config["documents"][i]
        archive = config["archives"][i]
        target = config["targets"][i]
        markdown = target + ".md"

        print(f"copy \t\t{relpath(doc)} \tto \t{relpath(archive)}")
        shutil.copy2(src=doc, dst=archive)
        
        print(f"unpack \t\t{relpath(archive)} \tto \t{relpath(target)}")
        shutil.unpack_archive(filename=archive, extract_dir=target)

        print(f"converting \t{relpath(doc)} \tto \t{relpath(markdown)}")
        convert(src=doc, dst=markdown)


if __name__ == "__main__":
    config = get_config()
    main(config)