#!/usr/bin/python3

import fnmatch
import os

import mediatrim.exif
import mediatrim.remove_duplicates
import mediatrim.rename


def print_files(files_list):
    for f in files_list:
        print('\t' + f)

def get_media_files_in_dir(work_dir):
    media_extensions = ['*.jpg', '*.jpeg', '*.png', '*.mp4', '*.avi']
    media_files = []
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            for ext in media_extensions:
                if fnmatch.fnmatch(file, ext):
                    media_files.append(os.path.join(root, file))

    return media_files


def main():
    print('=== MediaTrim =====')
    work_dir = os.getcwd()
    print('Work dir: ' + work_dir)
    print('Remove duplicates:')
    mediatrim.remove_duplicates.remove_duplicates_in_dir_recursively(work_dir)

    print('Seek media files in dir: ' + work_dir)
    media_files = get_media_files_in_dir(work_dir)

    print('Found media files:')
    print_files(media_files)

    print('Rename media files:')
    mediatrim.rename.rename_files(media_files)
    media_files = get_media_files_in_dir(work_dir)

    print('Remove exif data:')
    mediatrim.exif.remove_exif(media_files)


if __name__ == "__main__":
    main()
