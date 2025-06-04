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

def get_this_directory():
    return os.path.dirname(os.path.abspath(__file__))

THIS_DIRECTORY = get_this_directory()
CONFIG_PATH = os.path.join(THIS_DIRECTORY, "config.toml")

def get_toml() -> dict[str,Any]:
    with open(CONFIG_PATH,"rb") as file:
        config = tomllib.load(file)
    return config

def get_abs_path(path:str) -> str:
    return os.path.abspath(os.path.join(THIS_DIRECTORY, path))

def check_toml(config: dict[str, Any]):
    config["target"] = get_abs_path(config["target"])
    if not os.path.isdir(config["target"]):
        raise OSError(f"target: {config["target"]} not a directory")
    for i, file in enumerate(config["documents"]):
        file = config["documents"][i] = get_abs_path(file)
        if not os.path.isfile(file):
            raise OSError(f"documents: {file} not a file")
    for i, path in enumerate(config["measuring"]):
        path = config["measuring"][i] = get_abs_path(path)
        if not os.path.exists(path):
            raise OSError(f"measuring: {path} not a valid path")
    config["measurements"] = get_abs_path(config["measurements"])


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
