"""update a .tsv file on every call with the size and change in size of a .git directory"""

from argparse import Namespace
import os
from .config import get_config


def get_dir_size(start_path: str = '.') -> int:
    """returns the recusive size of a given directory"""
    total_size: int = 0
    if os.path.isfile(start_path):
        return os.path.getsize(start_path)
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def format_line(sizes: list[int], diffs: list[int]) -> str:
    """take size and diff and returns a line of .tsv format"""
    formatted_line = ""
    length:int = min(len(sizes), len(diffs))
    for i in range(length):
        formatted_line += f"{sizes[i]:,}\t{diffs[i]:,}\t"
    return formatted_line[:-1]


def unformat_line(line: str) -> tuple[list[int],list[int]]:
    """take line of .tsv format and return list of sizes and list of diffs"""
    sizes: list[int] = []
    diffs: list[int] = []
    cleaned_line: str = line.replace(',','')
    words: list[str] = cleaned_line.split()
    for i in range(len(words)):
        if i%2 == 0:
            sizes.append(int(words[i]))
        else:
            diffs.append(int(words[i]))
    return sizes, diffs

def get_last_line(saving_to_file:str) -> str:
    """get last line of the tsv file"""
    with open(saving_to_file, 'r') as f:
        lines = f.readlines()
        if len(lines) == 0:
            raise IndexError(f"{saving_to_file} has no lines")
        return lines[-1]


def get_last_sizes(saving_to_file:str) -> list[int]:
    """return size element of final row in tsv file"""
    sizes:list[int] = []
    try:
        last_line = get_last_line(saving_to_file=saving_to_file)
    except:
        sizes.append(0)
    else:
        sizes, diffs = unformat_line(last_line)
        _ = diffs
    return sizes
     

def append_line(saving_to_file:str, measuring:list[str]) -> str:
    """add a new row to the given tsv file, and return row"""
    last_sizes = get_last_sizes(saving_to_file)
    # pad last_sizes, in case of adding new file
    for i in range(len(measuring) - len(last_sizes)):
        last_sizes.append(0)
    # end
    new_sizes:list[int] = []
    diffs:list[int] = []
    for i, file in enumerate(measuring):
        new_sizes.append(get_dir_size(file))
        diffs.append(new_sizes[i] - last_sizes[i])
        
    line = format_line(new_sizes, diffs)
    with open(saving_to_file, 'a') as file:
        file.write(line+'\n')
    return line


def measure(args: Namespace):
    """add a new row to the tsv file, and print row"""
    config = get_config(args.CONFIG)
    SAVING_TO_FILE =  config["measurements"]
    MEASURING: list[str] = config["measuring"]
    line = append_line(saving_to_file=SAVING_TO_FILE, measuring=MEASURING)
    print(line)
    

def main():
    args = Namespace(CONFIG=".")
    measure(args)

if __name__ == "__main__":
    main()
