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
CONFIG_FILE_NAME = ".vccas.toml"


def get_toml(search_path: str) -> dict[str,Any]:
    if os.path.isfile(search_path):
        config_path = search_path
    elif os.path.isdir(search_path):
        config_path = os.path.join(search_path, CONFIG_FILE_NAME)
    else:
        raise FileNotFoundError(CONFIG_FILE_NAME + "not found")
    with open(config_path,"rb") as file:
        config = tomllib.load(file)
    return config

def get_abs_path(path:str) -> str:
    return os.path.abspath(os.path.join(THIS_DIRECTORY, path))

def process_toml(config: dict[str, Any]):
    config["target"] = get_abs_path(config["target"])
    for i, file in enumerate(config["documents"]):
        file = config["documents"][i] = get_abs_path(file)
    for i, path in enumerate(config["measuring"]):
        path = config["measuring"][i] = get_abs_path(path)
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
    
def get_config(search_path: str):
    config = get_toml(search_path=search_path)
    process_toml(config)
    get_dependent_variables(config)
    return config
    

def main():
    config = get_config(".")
    print(config)

if __name__ == "__main__":
    main()