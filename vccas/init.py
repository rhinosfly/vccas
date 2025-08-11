"""initialize example .vccas.toml in cwd"""

from argparse import Namespace


def init(args: Namespace | None = None):
    """initialze example .vccas.toml in cwd"""
    _ = args
    toml_text = """documents     = ["src/document1.docx", "src/document2.docx"]
target        = "extracted_files"
measuring     = [".git", "src/document1.docx"]
measurements  = "extracted_files/measurement.tsv"
"""
    path = ".vccas.toml"
    print(f"initializing {path}")
    with open(path, 'w') as file:
        file.write(toml_text)


if __name__ == "__main__":
    init()
