#!/usr/bin/python

import fnmatch
import os

import mediatrim.exif
import mediatrim.rename


def print_files(files_list):
    for f in files_list:
        print('\t' + f)


def main():
    print('=== MediaTrim =====')
    work_dir = os.getcwd()
    print('Seek media files in dir: ' + work_dir)

    media_files = []
    media_extensions = ['*.jpg', '*.jpeg', '*.png', '*.mp4', '*.avi']
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            for ext in media_extensions:
                if fnmatch.fnmatch(file, ext):
                    media_files.append(os.path.join(root, file))

    print('Found media files:')
    print_files(media_files)

    print('Remove exif data:')
    mediatrim.exif.remove_exif(media_files)

    print('Rename media files:')
    mediatrim.rename.rename_files(media_files)



if __name__ == "__main__":
    main()
