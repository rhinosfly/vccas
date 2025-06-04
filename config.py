''' global configuration variables'''

import tomllib
import os
from typing import Any

'''toml format:
documents = "filepath"
target = "directory path"
measuring = ["path1", "path2"]
measurements = "path"
'''
CONFIG_PATH = "config.toml"


def get_toml() -> dict[str,Any]:
    with open(CONFIG_PATH,"rb") as file:
        config = tomllib.load(file)
    return config


def check_toml(config: dict[str, Any]):
    for file in config["documents"]:
        if not os.path.isfile(file):
            raise OSError(f"documents: {file} not a file")
        if not os.path.isdir(config["target"]):
            raise OSError(f"target: {config["target"]} not a directory")
        for path in config["measuring"]:
            if not os.path.exists(path):
                raise OSError(f"measuring: {path} not a valid path")


def get_dependent_variables(config: dict[str, str|list[str]]):
    '''add more keys to config'''
    config["targets"] = []
    config["archives"] = []
    for doc in config["documents"]:
        basename:str = os.path.basename(doc)
        filename:str = os.path.splitext(basename)[0]
        target:str = os.path.join(str(config["target"]), filename)
        archive:str = target + ".zip"
        config["targets"].append(target)
        config["archives"].append(archive)
    del config["target"]
    
def get_config():
    config = get_toml()
    check_toml(config)
    get_dependent_variables(config)
    return config
    
if __name__ == "__main__":
    config = get_config()
    print(config)
