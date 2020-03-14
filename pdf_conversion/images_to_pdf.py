#!/usr/bin/env python 
 
import subprocess
import sys
import os
import img2pdf
import itertools
import shutil
import subprocess

def is_image(path):
    _, extname = os.path.splitext(path)
    return extname.lower() in ['.png', '.jpg', '.jpeg']

def is_image_or_text(path):
    _, extname = os.path.splitext(path)
    return is_image(path) or extname.lower() == '.txt'

def convert(dirpath, dist=None, lexical=False):
    if not dist:
        dist = os.path.abspath(dirpath) + '.pdf'

    images = [os.path.abspath(os.path.join(dirpath, i)) for i in os.listdir(dirpath) if not i.startswith('.')]
    if images and all(is_image_or_text(i) for i in images):
        images = [i for i in images if is_image(i)]
        for i in images:
            # img2pdf refuses to convert images with transparency
            if i.endswith('.png') or i.endswith('.PNG'):
                pre, _ = os.path.splitext(i)
                subprocess.check_call(['convert', i, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', pre + '.jpg'])
                os.remove(i)
        if lexical:
            images.sort()
        else:
            sort_images(images)
        with open(dist, "wb") as f: 
            f.write(img2pdf.convert(images)) 
            print(f"Created PDF file: {dist}")
            return True
    else:
        print(f"{dirpath} doesn't look like a directory of images. Skipped.")
        return False

def sort_images(images):
    def all_same(x): 
        return all(x[0] == y for y in x) 

    char_tuples = list(zip(*images))
    reversed_char_tuples = list(zip(*[reversed(i) for i in images]))

    prefix_tuples = itertools.takewhile(all_same, char_tuples)
    common_prefix = ''.join([t[0] for t in prefix_tuples])

    suffix_tuples = itertools.takewhile(all_same, reversed_char_tuples)
    common_suffix = ''.join([t[0] for t in suffix_tuples])[::-1]

    def page_number(x):
        x = x[len(common_prefix):]
        x = x[:-len(common_suffix)] if common_suffix else x
        a = x.split('-')
        if len(a) > 1:
            return (float(a[0]) + float(a[1])) / 2.0 # 1-2 => 1.5, yeah a stupid workaround
        else:
            return float(x)

    images.sort(key = page_number)

# Convert all in the current path:
# images_to_pdf.py
# Convert one directory:
# images_to_pdf.py [dir]
#   --lexical Sort images by lexicographical order

# When you need to preprocess file names manually:
# > import os
# > import re
# > os.chdir("YOUR_DIRECTIONARY")
# > files = os.dirlist('.')
# > for f in files:
# >     os.rename(f, re.sub(r".*p(\d+).*", r"\1.jpg", f)) # Just an example
 
def main():
    lexical = '--lexical' in sys.argv
    if len(sys.argv) > 1:
        path = os.path.abspath(sys.argv[1])
        succeeded = convert(path, lexical=lexical)        
        if succeeded:
            shutil.rmtree(path)
    else:
        dirpath = os.getcwd()
        files = os.listdir(dirpath)
        for f in files:
            print(f"Processing {f}")
            path = os.path.abspath(os.path.join(dirpath, f))
            if os.path.isdir(path):
                succeeded = convert(path, lexical=lexical)
                if succeeded:
                    shutil.rmtree(path)

if __name__ == "__main__":
    main()