#!/usr/bin/python

import os
import fnmatch

import mediatrim.rename

def print_files(files_list):
    print('Files to trim:')
    for f in files_list:
        print('\t' + f)


def main():
    print('=== MediaTrim =====')
    work_dir = os.getcwd()
    print('Seek files in dir: ' + work_dir)

    media_files = []
    media_extensions = ['*.jpg', '*.jpeg', '*.png', '*.mp4', '*.avi']
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            for ext in media_extensions:
                if fnmatch.fnmatch(file, ext):
                    media_files.append(os.path.join(root, file))

    print_files(media_files)

    print('Rename files')
    mediatrim.rename.rename_files(media_files)


if __name__ == "__main__":
    main()
