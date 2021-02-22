#!/usr/bin/python3

import hashlib
import os
import re
import subprocess
import sys
from datetime import datetime

debug = False

def cmd_available(name):
    try:
        with open(os.devnull, 'w') as output:
            subprocess.call([name], stdout=output, stderr=output)
    except OSError:
        return False
    return True

def get_md5sum(file):
    if not os.path.isfile(file):
        return None

    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_mediafile_create_datetime(file):
    dt1970 = datetime(1970, 1, 1)
    output = subprocess.Popen(['exiftool', file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

    min_dt = None
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
                continue

            if min_dt == None or dt < min_dt:
                min_dt = dt

    return min_dt

def datetime_to_timestamp(dt):
    if dt == None:
        return None

    dt1970 = datetime(1970, 1, 1)
    ts = int((dt - dt1970).total_seconds())
    return ts

def rename_pattern(selected_files, regexp, cnt):
    for old_name in selected_files:
        date_search = re.search(regexp, old_name, re.IGNORECASE)
 
        dt = get_mediafile_create_datetime(old_name)
        ts = datetime_to_timestamp(dt)
        new_name = date_search.group(1) + date_search.group(2).lower() + '.' + date_search.group(3).lower() + '.' + date_search.group(4).lower() + '_' + str(ts) + '.' + date_search.group(5).lower()

        while True:
            same_name = old_name == new_name
            same_md5 = get_md5sum(old_name) == get_md5sum(new_name)
            new_file_exists = os.path.isfile(new_name)

            if same_name and same_md5:
                break

            if not same_name and same_md5:
                subprocess.call(['rm', old_name])
                break

            if same_name or new_file_exists:
                ts = ts + 1
                new_name = dir_name + '/' + dt.strftime("%Y.%m.%d_" + str(ts) + '.' + file_ext).lower()
                continue

            if debug:
                print('Old name:' + old_name + ' | New name:' + new_name)
            else:
                print('Old name:' + os.path.basename(old_name) + ' | New name:' + os.path.basename(new_name))
                os.rename(old_name, new_name)

            cnt = cnt + 1
            break

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

#    regexp_exprs = ['^(.*/?)IMG_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
#                    '^(.*/?).*BURST(\\d\\d\\d\\d)(\\d\\d)(\\d\\d).+\\.(jpe?g)$',
#                    '^(.*/?).*BURST(\\d\\d\\d\\d)(\\d\\d)(\\d\\d).+\\_COVER.(jpe?g)$',
#                    '^(.*/?)PANO_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',  # PANO_20190902_115101.vr.jpg
#                    '^(.*/?)PHOTO_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
#                    '^(.*/?).*PORTRAIT_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
#                    '^(.*/?)MVIMG_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
#                    '^(.*/?)Pic_(\\d\\d\\d\\d)_(\\d\\d)_(\\d\\d)_.+\\.(jpe?g)$',
#                    '^(.*/?)VID_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(mp4)$',
#                    '^(.*/?)(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)-.+\\.(mp4)$',
#                    ]

    cnt = 1
    for regexp in regexp_exprs:
        selected_files = list(filter(re.compile(regexp).search, files_list))
        if len(selected_files) == 0:
            continue

        cnt = cnt + rename_pattern(selected_files, regexp, cnt)

    return cnt

def rename_using_exif(files_list, cnt):
    not_renamed = []
    for old_name in files_list:
        dt = get_mediafile_create_datetime(old_name)
        if dt != None:
            dir_name = os.path.dirname(old_name)
            file_name = os.path.basename(old_name)
            file_ext = file_name.split(".")[-1]
            ts = datetime_to_timestamp(dt)
            new_name = dir_name + '/' + dt.strftime("%Y.%m.%d_" + str(ts) + '.' + file_ext).lower()

            while True:
                same_name = old_name == new_name
                same_md5 = get_md5sum(old_name) == get_md5sum(new_name)
                new_file_exists = os.path.isfile(new_name)

                if same_name and same_md5:
                    break

                if not same_name and same_md5:
                    subprocess.call(['rm', old_name])
                    break

                if same_name or new_file_exists:
                    ts = ts + 1
                    new_name = dir_name + '/' + dt.strftime("%Y.%m.%d_" + str(ts) + '.' + file_ext).lower()
                    continue

                if debug:
                    print('Old name:' + old_name + ' | New name:' + new_name)
                else:
                    print('Old name:' + os.path.basename(old_name) + ' | New name:' + os.path.basename(new_name))
                    os.rename(old_name, new_name)

                cnt = cnt + 1
                break
        else:
            not_renamed.append(old_name)

    return not_renamed, cnt

def rename_files(files_list):
    exif_cnt = 0
    files_list, exif_cnt = rename_using_exif(files_list, exif_cnt)
    print('Renamed using exif: ' + str(exif_cnt) + '\n')

    pattern_cnt = 0
    if len(files_list) > 0:

        pattern_cnt = rename_using_patterns(files_list, pattern_cnt)
        print('Renamed using patterns: ' + str(pattern_cnt))
        print('')

    print('Total renamed: ' + str(exif_cnt + pattern_cnt))


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
