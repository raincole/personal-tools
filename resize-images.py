#!/usr/bin/env python

import click
import subprocess
import os.path 

MAX_RESOLUTION = "4000x3000"
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

@click.command()
@click.argument("path", required=True, type=click.Path())
@click.option("--max-resolution", default=MAX_RESOLUTION, help="The max resolution after resizing (aspect ratio preserved)")
def recursive_resize(path, max_resolution):
    """Recursively resize images in a directory"""

    for root, subdirs, files in os.walk(path):
        for f in files:
            _, ext = os.path.splitext(f)
            if ext.lower() in IMAGE_EXTENSIONS:
                filepath = os.path.join(root, f)
                subprocess.run(["convert", filepath, "-resize", max_resolution, filepath])
                print("Resizing " + filepath + " ...")

if __name__ == '__main__':
    recursive_resize()