# -*- coding=utf-8

import os
import threading

from util import sbutils
from util import ioutils

DATA_PATH = 'D:/data/stock/'
STEP = 10


class Crawler(threading.Thread):
    def __init__(self, start_pos, end_pos, step):
        threading.Thread.__init__(self)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.step = step

    def run(self):
        for cur in range(self.start_pos, self.end_pos, self.step):
            try:
                thread_name = threading.currentThread().getName()
                sub_start = cur
                sub_end = sub_start + STEP
                for i in range(sub_start, sub_end):
                    stock_id = sbutils.get_stock_name(i)
                    # stock_id = sbutils.get_stock_id(i)
                    line = sbutils.get_stock_history_data(stock_id, 0, sbutils.get_current_timestamp())
                    if len(line) > 5:
                        print(thread_name, i, '/', sub_end, ", id : ", stock_id, " downloaded.")
                        file_name = DATA_PATH + stock_id + '.txt'
                        ioutils.write_line_to_file(file_name, line)
                        print(thread_name, "File saved, ", file_name)
            except Exception as e:
                print(thread_name, "error,", e)


def get_last_crawled_stock_id():
    files = os.listdir(DATA_PATH)
    files.sort(reverse=True)
    if len(files) != 0:
        first = files[0][2:]
        first = first.strip('.txt')
        return int(first)


def main():
    start_stock_id = 000000
    end_stock_id = 1000
    print("crawled stock id : %d" % start_stock_id)

    threads = []
    count = 5

    for i in range(0, count):
        threads.append(Crawler(start_stock_id + STEP * i, end_stock_id, STEP * count))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
