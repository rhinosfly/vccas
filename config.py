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

CONFIG_FILE_NAME = ".vccas.toml"


def get_toml(config_file: str) -> dict[str,Any]:
    with open(config_file,"rb") as file:
        config = tomllib.load(file)
    return config


def rectify_paths(config: dict[str, Any], config_dir: str):
    config["target"] = os.path.join(config_dir, config["target"])
    for i, file in enumerate(config["documents"]):
        config["documents"][i] = os.path.join(config_dir, file)
    for i, path in enumerate(config["measuring"]):
        config["measuring"][i] = os.path.join(config_dir, path)
    config["measurements"] = os.path.join(config_dir, config["measurements"])


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
    # get path and filename
    if os.path.isfile(search_path):
        config_dir = os.path.dirname(search_path)
        config_file = search_path
    elif os.path.isdir(search_path):
        config_dir = search_path
        config_file = os.path.join(search_path, CONFIG_FILE_NAME)
    else:
        raise FileNotFoundError(CONFIG_FILE_NAME + "not found")
    # get config
    config = get_toml(config_file=config_file)
    rectify_paths(config=config, config_dir=config_dir)
    get_dependent_variables(config)
    return config
    

def main():
    config = get_config(".")
    print(config)

if __name__ == "__main__":
    main()