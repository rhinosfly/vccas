''' global configuration variables'''

import tomllib
import os

'''toml format:
document_path = "filepath"
unzipped_files_path = "directory path"
measuring_paths = ["path1", "path2"]
'''
CONFIG_PATH = "config.toml"


def get_toml() -> dict[str,str]:
    #get data
    with open(CONFIG_PATH,"rb") as file:
        config = tomllib.load(file)
    return config


def check_toml(config: dict):
    if not os.path.isfile(config["document_path"]):
        raise OSError(f"document_path: {config["document_path"]} not a file")
    if not os.path.isdir(config["unzipped_files_path"]):
        raise OSError(f"unzipped_files_path: {config["unzipped_files_path"]} not a directory")
    for path in config["measuring_paths"]:
        if not os.path.exists(path):
            raise OSError(f"measuring_paths: {path} not a valid path")


def get_dependent_variables(config: dict) -> dict:
    '''add more keys to config'''
    basename = os.path.basename(config["document_path"])
    filename = os.path.splitext(basename)[0]
    config["filename"] = filename
    
    
def get_config():
    config = get_toml()
    check_toml(config)
    get_dependent_variables(config)
    return config
    
if __name__ == "__main__":
    config = get_config()
    print(config)
