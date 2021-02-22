#!/usr/bin/python3

import os
import subprocess
import sys


def cmd_available(name):
    try:
        with open(os.devnull, 'w') as output:
            subprocess.call([name], stdout=output, stderr=output)
    except OSError:
        return False
    return True


def remove_exif_on_file(file):
    print('\t' + file)
    devnull = open(os.devnull, 'w')
    subprocess.call(['exiftool', '-overwrite_original',
                     '-Make=',
                     '-Model=',
                     '-GPS*=',
                     '-Gps*=',
                     '-gps*=',
                     '-CreateDate=',
                     '-DateTimeOriginal=',
                     '-Software=',
                     '-ImageDescription=',
                     '-SubSecCreateDate=',
                     '-SubSecDateTimeOriginal=',
                     '-SubSecModifyDate=',
                     '-ICC_Profile:all=',
                     '-Photoshop:all=',
                     '-XMP:all=',
                     '-IPTC:all=',
                     '-MakerNotes:all=',
                     file], stdout=devnull, stderr=subprocess.STDOUT)


def remove_exif(file_list):
    for file in file_list:
        remove_exif_on_file(file)

    print('Total updated files: ' + str(len(file_list)))

def main():
    if not cmd_available('exiftool'):
        print('\033[91m {}\033[00m'.format('** No exiftool command available on this machine'))
        print('\033[91m {}\033[00m'.format('** Please run \'sudo apt install exiftool\''))
        return

    work_dir = os.getcwd()

    if len(sys.argv) > 1:
        print('Removing exif data on media files')
        for file in sys.argv[1:]:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.mp4'):
                remove_exif_on_file(file)
    else:
        all_img_files = []
        for dir, subdirs, files in os.walk(work_dir):
            for file in files:
                all_img_files.append(file)

        remove_exif(all_img_files)


if __name__ == '__main__':
    main()
