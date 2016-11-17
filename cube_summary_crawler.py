# -*- coding=utf-8

import ioutils
import sbutils
import time
import os

#DATA_PATH = '/home/liyang/data/cube_summary'
DATA_PATH = 'D:/data/cube_summary'
ERROR_PATH = 'D:/data/cube_summary_error'
STEP = 100
END_POS = 200000


def gen_file_name(start, end):
    return '%s/%s_%s.txt' % (DATA_PATH, start, end)


def get_last_crawled_cube_id():
    files = os.listdir(DATA_PATH)
    files.sort(reverse=True)
    if len(files) != 0:
        pos = files[0].index('_')
        if pos == -1:
            print("file name error: %s", files[0])
        first = files[0][0:pos]
        return int(first)


def main():
    start_cube_id = sbutils.get_cube_start_pos()
    last_cube_id = get_last_crawled_cube_id()
    if last_cube_id and last_cube_id > start_cube_id:
        start_cube_id = last_cube_id
    print("crawled cube id : %d" % start_cube_id)
    for cur in range(start_cube_id, END_POS, STEP):
        try:
            lines = []
            sub_start = cur
            sub_end = sub_start + STEP
            for i in range(sub_start, sub_end):
                cube_id = sbutils.get_cube_id(i)
                line = sbutils.get_cube_summary(cube_id)
                lines.append(line)
                print("cube id : ", cube_id, " downloaded.")
                # time.sleep(1)
            file_name = gen_file_name(sub_start, sub_end)
            ioutils.write_lines_to_file(file_name, lines)
            print("File saved, ", file_name)
        except Exception:
            ioutils.write_lines_to_file(file_name + ".err", lines)

if __name__ == "__main__":
    main()

