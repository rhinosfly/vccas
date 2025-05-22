"""update a .tsv file on every call with the size and change in size of a .git directory"""

from genericpath import isfile
import os


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


def format_line(git_size:int, doc_size:int, git_diff:int, doc_diff:int) -> str:
    """take size and diff and returns a line of .tsv format"""
    formatted_line =  (f'{git_size:,}\t{doc_size:,}\t{git_diff:,}\t{doc_diff:,}')
    return formatted_line


def unformat_line(line: str) -> tuple[int, int, int, int]:
    """take line of .tsv format and return size and diff"""
    cleaned_line: str = line.replace(',','')
    words: list[str] = cleaned_line.split()
    git_size, doc_size, git_diff, doc_diff = words
    vars =  (int(git_size), int(doc_size), int(git_diff), int(doc_diff))
    return vars

def get_last_line(saving_to_file:str) -> str:
    """get last line of the tsv file"""
    with open(saving_to_file, 'r') as f:
        lines = f.readlines()
        if len(lines) == 0:
            raise IndexError(f"{saving_to_file} has no lines")
        return lines[-1]


def get_last_sizes(saving_to_file:str) -> tuple[int,int]:
    """return size element of final row in tsv file"""
    try:
        last_line = get_last_line(saving_to_file=saving_to_file)
    except:
        last_git_size = last_doc_size = 0
    else:
        last_git_size, last_doc_size,_,_ = unformat_line(last_line)
    return last_git_size, last_doc_size
     

def append_line(saving_to_file:str, measuring_file1:str, measuring_file2:str) -> str:
    """add a new row to the given tsv file, and return row"""
    last_git_size, last_doc_size = get_last_sizes(saving_to_file)
    git_size = get_dir_size(measuring_file1)
    doc_size = get_dir_size(measuring_file2)
    git_diff = git_size - last_git_size
    doc_diff = doc_size - last_doc_size
    line = format_line(git_size=git_size, doc_size=doc_size, git_diff=git_diff, doc_diff=doc_diff)
    with open(saving_to_file, 'a') as file:
        file.write(line+'\n')
    return line


def main() -> None:
    """add a new row to the tsv file, and print row"""
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    SAVING_TO_FILE =  DIR_PATH + "/../target/size.tsv"
    MEASURING_FILE1 = DIR_PATH + "/../.git"
    MEASURING_FILE2 = DIR_PATH  + "/../target/RSR00114_Rev. 3 (Test Report, TCD, AC Power Testing).zip"
    line = append_line(saving_to_file=SAVING_TO_FILE, measuring_file1=MEASURING_FILE1, measuring_file2=MEASURING_FILE2)
    print(line)
    

if __name__ == "__main__":
    main()
