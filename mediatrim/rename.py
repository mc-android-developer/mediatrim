#!/usr/bin/python

import hashlib
import os
import re
import subprocess
import sys
from datetime import datetime


def cmd_available(name):
    try:
        with open(os.devnull, 'w') as output:
            subprocess.call([name], stdout=output, stderr=output)
    except OSError:
        return False
    return True

def get_create_timestamp(file):
    output = subprocess.Popen(['exiftool', file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

    min_ts = sys.maxint
    for s in output.split('\n'):
        if 'Create Date' in s:
            s = s.split(' : ')[1]
            s = s.split('-')[0]
            s = s.split('.')[0]
            s = s.strip()
            try:
                dt = datetime.strptime(s, '%Y:%m:%d %H:%M:%S')
            except ValueError:
                dt = None   

            ts = int((dt - datetime(1970, 1, 1)).total_seconds())
            if ts < min_ts:
                min_ts = ts

    return min_ts

def rename_pattern(selected_files, regexp, cnt):
    for old_name in selected_files:
        date_search = re.search(regexp, old_name, re.IGNORECASE)
        cnt = cnt + 1
 
        ts = get_create_timestamp(old_name)
        new_name = date_search.group(1) + date_search.group(2).lower() + '.' + date_search.group(3).lower() + '.' + date_search.group(4).lower() + '_' + str(ts) + '.' + date_search.group(5).lower()
        while os.path.isfile(new_name):
            ts = ts + 1
            new_name = date_search.group(1) + date_search.group(2).lower() + '.' + date_search.group(3).lower() + '.' + date_search.group(4).lower() + '_' + str(ts) + '.' + date_search.group(5).lower()

        print('Old name:' + os.path.basename(old_name) + ' | New name:' + os.path.basename(new_name))
        os.rename(old_name, new_name)

    return cnt


def rename_files(files_list):
    regexp_exprs = ['^(.*/)\\d*.?IMG_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/)\\d*.?IMG_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)\\d+_COVER.(jpe?g)$',
                    '^(.*/)\\d*.?IMG_\\d+_BURST(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)\\d+_COVER.(jpe?g)$',
                    '^(.*/)\\d*.?PORTRAIT_\\d+_BURST(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)\\d+.(jpe?g)$',
                    '^(.*/)\\d*.?PORTRAIT_\\d+_BURST(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)\\d+_COVER.(jpe?g)$',
                    '^(.*/)PANO_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/)PHOTO_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/)MVIMG_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/)Pic_(\\d\\d\\d\\d)_(\\d\\d)_(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/)VID_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(mp4)$',
                    '^(.*/)VIDEO_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(mp4)$',
                    '^(.*/)(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)-.+\\.(mp4)$',
                    ]

    cnt = 1
    for regexp in regexp_exprs:
        selected_files = list(filter(re.compile(regexp).search, files_list))
        if len(selected_files) == 0:
            continue

        cnt = rename_pattern(selected_files, regexp, cnt)
        print('Renamed: ' + str(cnt - 1))
        print('')

    print('Total renamed: ' + str(cnt - 1))


def main():
    if not cmd_available('exiftool'):
        print('\033[91m {}\033[00m'.format('** No exiftool command available on this machine'))
        print('\033[91m {}\033[00m'.format('** Please run \'sudo apt install exiftool\''))
        return
    
    work_dir = os.getcwd()
    print('Rename files in dir: ' + work_dir)

    all_img_files = []
    for dir, subdirs, files in os.walk(work_dir):
        for file in files:
            all_img_files.append(dir + '/' + file)

    rename_files(all_img_files)


if __name__ == "__main__":
    main()
