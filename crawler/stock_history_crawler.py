from util import sbutils
from util import ioutils


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
                lines = []
                sub_start = cur
                sub_end = sub_start + STEP
                for i in range(sub_start, sub_end):
                    stock_id = sbutils.get_stock_name(i)
                    # stock_id = sbutils.get_stock_id(i)
                    line = sbutils.get_stock_history_data(stock_id)
                    lines.append(line)
                    print(thread_name, i, '/', sub_end, ", id : ", stock_id, " downloaded.")
                    file_name = stock_id + '.txt'
                    ioutils.write_line_to_file(file_name, lines)
                    print(thread_name, "File saved, ", file_name)
            except Exception as e:
                print(thread_name, "error,", e)


def get_last_crawled_stock_id():
    files = os.listdir(DATA_PATH)
    files.sort(reverse=True)
    if len(files) != 0:
        first = files[0][2:]
        return int(first)


def main():
    start_stock_id = 600000
    last_stock_id = get_last_crawled_stock_id()
    if last_stock_id and last_stock_id > start_stock_id:
        start_stock_id = last_stock_id
    print("crawled stock id : %d" % start_stock_id)

    threads = []
    count = 1

    for i in range(0, count):
        threads.append(Crawler(start_stock_id + STEP * i, END_POS, STEP * count))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
