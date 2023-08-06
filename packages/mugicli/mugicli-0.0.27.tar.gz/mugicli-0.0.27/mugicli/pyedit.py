import argparse
from bashrange import expand_args
import tempfile
from . import read_stdin_text
import os
from .shared import has_magic, glob_paths_files
import glob
import subprocess
import shutil

def main():
    EXAMPLE_TEXT = """examples: pygrep test | pyedit
"""

    parser = argparse.ArgumentParser(prog="pyedit", description="", epilog=EXAMPLE_TEXT, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("src", nargs="*")
    
    args = parser.parse_args(expand_args())

    paths = []

    if len(args.src) == 0:
        temp = tempfile.mkdtemp()
        path = os.path.join(temp, "text.txt")
        with open(path, "w") as f:
            f.write(read_stdin_text())
        paths.append(path)
    else:
        paths = glob_paths_files(args.src)

    code = shutil.which("code.exe")
    if code is None:
        guess = os.path.join(os.environ['localappdata'], "Programs", "Microsoft VS Code", "Code.exe")
        if os.path.isfile(guess):
            code = guess

    if code is None:
        raise Exception("code.exe not found")

    for path in paths:
        subprocess.run([code,"-r","-g",path])

    #print(args)

if __name__ == "__main__":
    main()