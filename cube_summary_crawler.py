# -*- coding=utf-8

import ioutils
import sbutils
import time
import threading
import os

#DATA_PATH = '/home/liyang/data/cube_summary'
DATA_PATH = '/home/liyang/data/cube_summary_sp'
#DATA_PATH = 'D:/data/cube_summary'
ERROR_PATH = 'D:/data/cube_summary_error'
STEP = 100
END_POS = 2000000


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


class Crawler(threading.Thread):

    def __init__(self, start_pos, end_pos, step):
        threading.Thread.__init__(self)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.step = step


    def run(self):
        for cur in range(self.start_pos, self.end_pos, self.step):
            try:
                threadname = threading.currentThread().getName()
                lines = []
                sub_start = cur
                sub_end = sub_start + STEP
                file_name = gen_file_name(sub_start, sub_end)
                for i in range(sub_start, sub_end):
                    cube_id = sbutils.get_sp_cube_id(i)
                    # cube_id = sbutils.get_cube_id(i)
                    line = sbutils.get_cube_summary(cube_id)
                    lines.append(line)
                    print(threadname, i, '/', sub_end, ", cube id : ", cube_id, " downloaded.")
                    # time.sleep(1)
                ioutils.write_lines_to_file(file_name, lines)
                print(threadname, "File saved, ", file_name)
            except Exception as e:
                print(threadname, "error,", e)
                ioutils.write_lines_to_file(file_name + ".err", lines)

def main():
    start_cube_id = sbutils.get_cube_start_pos()
    last_cube_id = get_last_crawled_cube_id()
    if last_cube_id and last_cube_id > start_cube_id:
        start_cube_id = last_cube_id
    print("crawled cube id : %d" % start_cube_id)

    threads = []
    count = 1

    for i in range(0, count):
        threads.append(Crawler(start_cube_id + STEP * i, END_POS, STEP * count))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()

