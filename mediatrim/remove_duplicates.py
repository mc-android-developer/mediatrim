#!/usr/bin/python

import hashlib
import os
import subprocess
import sys


def get_md5sum(file):
    if not os.path.isfile(file):
        return None

    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_duplicates(file_list):
    files_md5 = {}
    cnt = 0
    for file in file_list:
        md5sum = get_md5sum(file)
        if md5sum in files_md5.keys():
            files_md5[md5sum].append(file)
        else:
            files_md5[md5sum] = [file]

    for key in files_md5:
        duplicates = files_md5[key]
        if (len(duplicates) > 1):
            # remove smallest file from duplicates
            duplicates.remove(min((word for word in duplicates if word), key=len))
            # remove other duplicates
            for file in duplicates:
                print('\t\tRemove duplicate: ' + file)
                cnt += 1
                subprocess.call(['rm', file])

    print('\t\t' + str(cnt) + ' duplicates removed')


def remove_duplicates_in_dir(directory):
    print('\tRemove duplicates in folder: ' + directory)
    dir_files = []
    for dir, subdirs, files in os.walk(directory):
        if dir == directory:
            for file in files:
                dir_files.append(dir + '/' + file)

    remove_duplicates(dir_files)


def remove_duplicates_in_dir_recursively(directory):
    all_dirs = {directory}
    for dir, subdirs, files in os.walk(directory):
        all_dirs.add(dir)

    for d in all_dirs:
        remove_duplicates_in_dir(d)


def main():
    work_dir = os.getcwd()

    if len(sys.argv) > 1:
        remove_duplicates(sys.argv[1:])
    else:
        remove_duplicates_in_dir_recursively(work_dir)


if __name__ == '__main__':
    main()
