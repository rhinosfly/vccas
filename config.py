''' global configuration variables'''

import tomllib
import os

'''toml format:
documents = "filepath"
target = "directory path"
measuring = ["path1", "path2"]
'''
CONFIG_PATH = "config.toml"


def get_toml() -> dict[str,str]:
    #get data
    with open(CONFIG_PATH,"rb") as file:
        config = tomllib.load(file)
    return config


def check_toml(config: dict):
    for file in config["documents"]:
        if not os.path.isfile(file):
            raise OSError(f"documents: {file} not a file")
        if not os.path.isdir(config["target"]):
            raise OSError(f"target: {config["target"]} not a directory")
        for path in config["measuring"]:
            if not os.path.exists(path):
                raise OSError(f"measuring: {path} not a valid path")


def get_dependent_variables(config: dict) -> dict:
    '''add more keys to config'''
    config["targets"] = []
    config["archives"] = []
    for doc in config["documents"]:
        basename = os.path.basename(doc)
        filename = os.path.splitext(basename)[0]
        target = os.path.join(config["target"], filename)
        archive = target + ".zip"
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
