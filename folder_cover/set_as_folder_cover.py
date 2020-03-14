#!/usr/bin/env python 
 
import sys
import os
import subprocess
import tempfile
from PIL import Image, ImageOps, ImageChops
import numpy
import blend_modes


def is_image(path):
    _, extname = os.path.splitext(path)
    return extname.lower() in ['.png', '.jpg', '.jpeg']

def blend_cover(cover: Image.Image, folder: Image.Image, margin=80):
    dest_size = tuple((d - margin * 2 for d in folder.size))
    cover1 = ImageOps.pad(cover, dest_size, method=Image.BICUBIC)
    cover2 = ImageOps.expand(cover1, margin)

    cover_float = numpy.array(cover2).astype(float)
    folder_float = numpy.array(folder).astype(float)
    blended_float = blend_modes.overlay(folder_float, cover_float, 1)
    blended_array = numpy.uint8(blended_float)
    blended_img = Image.fromarray(blended_array)

    # The transparent area isn't blended, so we manually paste the cover upon it
    cover3 = Image.new("RGBA", cover2.size)
    cover3.paste(cover2, mask=ImageChops.invert(blended_img))
    blended_img.alpha_composite(cover3)

    return blended_img


def main():
    FOLDER_ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "folder_icon.png")
    path = os.path.abspath(sys.argv[1])
    with tempfile.TemporaryDirectory() as tempdir:
        if not is_image(path):
            subprocess.run(["qlmanage", "-t", "-f", "8", path, "-o", tempdir], check=True)
            path = os.path.join(tempdir, path + ".png")

        cover = Image.open(path).convert("RGBA")
        folder_icon = Image.open(FOLDER_ICON_PATH) 
        blended = blend_cover(cover, folder_icon)

        icon_path = os.path.join(tempdir, "icon.png")
        blended.save(icon_path)

        subprocess.run(["fileicon", "set", os.path.dirname(path), icon_path])

if __name__ == "__main__":
    main()