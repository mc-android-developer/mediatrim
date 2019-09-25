#!/usr/bin/python

import os
import fnmatch

import imgtrim.rename

def print_files(files_list):
    print('Files to trim:')
    for f in files_list:
        print('\t' + f)


def main():
    print('=== ImgTrim =====')
    work_dir = os.getcwd()
    print('Seek files in dir: ' + work_dir)

    img_files = []
    img_extensions = ['*.jpg', '*.jpeg', '*.png']
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            for ext in img_extensions:
                if fnmatch.fnmatch(file, ext):
                    img_files.append(os.path.join(root, file))

    print_files(img_files)

    print('Rename files')
    imgtrim.rename.rename_files(img_files)


if __name__ == "__main__":
    main()
