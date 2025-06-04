'''extract zip archive into docx'''
import shutil
from os.path import relpath
from typing import Any

from config import get_config


def main(config: dict[str,Any]):
    for i in range(len(config["documents"])):
        doc = config["documents"][i]
        archive = config["archives"][i]
        target = config["targets"][i]

        print(f"move {relpath(doc)} to {relpath(archive)}")
        shutil.copy2(src=doc, dst=archive)
        
        print(f"unpack {relpath(archive)} to {relpath(target)}")
        shutil.unpack_archive(filename=archive, extract_dir=target)


if __name__ == "__main__":
    config = get_config()
    main(config)