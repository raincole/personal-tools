#!/usr/bin/env python

import subprocess
import sys
import os

def unarchive(path, dist=None):
    if not dist:
        dist = os.path.dirname(path)
    exit_code = subprocess.check_call(['unar', f"{path}", '-output-directory', f"{dist}"]) 
    return True if exit_code == 0 else False

# Unarchive all in the current path:
# unar_crb_cbz.py
# Unarchive one file:
# unar_crb_cbz.py [crb_or_cbz_file]
 
def main():
    if len(sys.argv) > 1:
        path = os.path.abspath(sys.argv[1])
        succeeded = unarchive(path)
        if not succeeded:
            print(f"Abort! An error happened when unarchving {path}")
    else:
        dirpath = os.getcwd()
        files = os.listdir(dirpath)
        for f in files:
            path = os.path.abspath(os.path.join(dirpath, f))
            _, extname = os.path.splitext(path)
            if extname in ['.cbr', '.cbz', '.CBR', '.CBZ', '.zip', '.ZIP', '.rar', '.RAR']:
                succeeded = unarchive(path)
                if not succeeded:
                    print(f"Abort! An error happened when unarchving {path}")
                    break
                else:
                    os.remove(path)


if __name__ == "__main__":
    main()