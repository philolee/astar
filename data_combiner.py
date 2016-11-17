import os
import json
import pandas as pd
import time
import matplotlib.pyplot as plt


class DataCombiner:
    data = []

    def load_data(self, path):
        self.data = []
        files = os.listdir(path)
        for file in files:
            file_name = path + '/' + file
            text = open(file_name, 'r', encoding='utf-8').read()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if line:
                        raw_obj = json.loads(line)
                        new_obj = self.__parse_raw_data(raw_obj)
                        self.data.append(new_obj)

    def __parse_raw_data(self, raw_obj):
        new_obj = {}
        new_obj['id'] = raw_obj['id']
        new_obj['name'] = raw_obj['name']
        new_obj['symbol'] = raw_obj['symbol']
        new_obj['active_flag'] = raw_obj['active_flag']
        new_obj['created_at'] = self.__to_format_time(raw_obj['created_at'])
        new_obj['updated_at'] = self.__to_format_time(raw_obj['updated_at'])
        new_obj['daily_gain'] = raw_obj['daily_gain']
        new_obj['market'] = raw_obj['market']
        new_obj['monthly_gain'] = raw_obj['monthly_gain']
        new_obj['total_gain'] = raw_obj['total_gain']
        new_obj['net_value'] = raw_obj['net_value']
        new_obj['rank_percent'] = raw_obj['rank_percent']
        new_obj['follower_count'] = raw_obj['follower_count']
        new_obj['close_date'] = raw_obj['close_date']
        return new_obj

    def __to_format_time(self, timestamp):
        time_array = time.localtime(float(timestamp) / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def draw(df):
    rows = []
    for i in range(-100, 500, 10):
        row = {}
        row['gain'] = i
        row['count'] = len(df[(df.total_gain > i) & (df.total_gain <= i + 10)].index)
        rows.append(row)

    data = pd.DataFrame(rows, columns=['gain', 'count'])
    data = data.set_index('gain')
    data['count'].plot()
    plt.show()
    print('ok')


def main():
    combiner = DataCombiner()
    combiner.load_data('D:/data/cube_summary')
    # combiner.load_data('D:/data/test')
    df = pd.DataFrame(combiner.data,
                      columns=['id', 'name', 'symbol', 'net_value', 'total_gain', 'rank_percent', 'follower_count',
                               'active_flag', 'created_at', 'updated_at', 'daily_gain', 'monthly_gain', 'close_date', 'market'])
    df = df.sort_values(by='net_value', ascending=False)
    df = df[df.market == 'cn']
    df.to_csv('1.csv')
    draw(df)


if __name__ == '__main__':
    main()
