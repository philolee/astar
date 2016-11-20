# -*- coding=utf-8

import os
import json
import pandas as pd
import datetime
import threading


class StockHistoryToDF(threading.Thread):
    file_names = []
    input_path = ''
    output_path = ''

    def __init__(self, input_path, output_path, file_names):
        threading.Thread.__init__(self)
        self.file_names = file_names
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        for file_name in self.file_names:
            text = open(self.input_path + file_name, 'r', encoding='utf-8').read()
            raw_obj = json.loads(text)
            chartlist = raw_obj['chartlist']
            for one in chartlist:
                one['date'] = self.__convert_to_date(one['time'])
                del one['time']
            df = pd.DataFrame(chartlist)
            out_name = self.output_path + raw_obj['stock']['symbol'] + '.csv'
            df.to_csv(out_name)
            print("Thread:", threading.currentThread().getName(), ' ', out_name + ' done.')

    def __convert_to_date(self, timestr):
        # timestr = 'Mon Jan 07 00:00:00 +0800 1991'
        format = '%a %b %d %H:%M:%S %z %Y'
        d = datetime.datetime.strptime(timestr, format)
        return d.strftime('%Y-%m-%d')


def split_list(a_list, n):
    results = []
    for i in range(0, n):
        ret = []
        results.append(ret)
    for a in range(0, len(a_list)):
        results[a % n].append(a_list[a])
    return results


def main():
    input_path = 'D:/data/stock/'
    output_path = 'D:/data/stock_history_df/'
    file_names = os.listdir(input_path)

    count = 20
    results = split_list(file_names, count)

    threads = []

    for i in range(0, count):
        threads.append(StockHistoryToDF(input_path, output_path, results[i]))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print('ok')


if __name__ == '__main__':
    main()
