#!/usr/bin/python

import os
import re


def rename_pattern(selected_files, regexp, cnt):
    for old_name in selected_files:
        date_search = re.search(regexp, old_name, re.IGNORECASE)
        new_name = date_search.group(1) + date_search.group(2) + '.' + date_search.group(3) + '.' + date_search.group(4) + '_' + str(cnt) + '.' + date_search.group(5)
        print('Old name:' + os.path.basename(old_name) + ' | New name:' + os.path.basename(new_name))
        os.rename(old_name, new_name)
        cnt = cnt + 1
    return cnt


def rename_files(files_list):
    regexp_exprs = ['^(.*/?)IMG_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/?).*BURST(\\d\\d\\d\\d)(\\d\\d)(\\d\\d).+\\_COVER.(jpe?g)$',
                    '^(.*/?)PANO_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',  # PANO_20190902_115101.vr.jpg
                    '^(.*/?)PHOTO_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/?)MVIMG_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/?)Pic_(\\d\\d\\d\\d)_(\\d\\d)_(\\d\\d)_.+\\.(jpe?g)$',
                    '^(.*/?)VID_(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)_.+\\.(mp4)$',
                    '^(.*/?)(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)-.+\\.(mp4)$',
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
    work_dir = os.getcwd()
    print('Rename files in dir: ' + work_dir)

    all_img_files = []
    for dir, subdirs, files in os.walk(work_dir):
        for file in files:
            all_img_files.append(dir + '/' + file)

    rename_files(all_img_files)


if __name__ == "__main__":
    main()
