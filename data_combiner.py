import os
import json
import pandas as pd
import time
import matplotlib.pyplot as plt


class DataCombiner:
    meta_data = []
    holding_data = []
    path = ''
    meta_data_df = ''
    holding_data_df = ''

    def __init__(self, path):
        self.path = path
        pipelines = [
            {'method': self.__parse_meta_data, 'data': self.meta_data},
            {'method': self.__parse_holding_data, 'data': self.holding_data}
        ]
        self.__load_data(pipelines)

        self.__gen_meta_dataframe()
        self.__gen_holding_data()

    def __gen_meta_dataframe(self):
        df = pd.DataFrame(self.meta_data,
                          columns=['id', 'name', 'symbol', 'net_value', 'total_gain', 'rank_percent', 'follower_count',
                                   'active_flag', 'created_at', 'updated_at', 'daily_gain', 'monthly_gain',
                                   'close_date', 'market'])
        df = df.sort_values(by='net_value', ascending=False)
        df = df[(df.market == 'cn') & (df.close_date == '')]
        df = df.drop_duplicates()
        self.meta_data_df = df

    def __gen_holding_data(self):
        df = pd.DataFrame(self.holding_data,
                          columns=['weight', 'segment_name', 'stock_name', 'stock_symbol', 'id', 'name', 'symbol',
                                   'created_at', 'close_date', 'market'])
        df = df[df.market == 'cn']
        df = df.drop_duplicates()
        self.holding_data_df = df

    def __load_data(self, pipelines):
        files = os.listdir(self.path)
        for file in files:
            file_name = self.path + '/' + file
            text = open(file_name, 'r', encoding='utf-8').read()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if line:
                        raw_obj = json.loads(line)
                        for pipeline in pipelines:
                            parse_method = pipeline['method']
                            data = pipeline['data']
                            parse_method(raw_obj, data)

    def __parse_meta_data(self, raw_obj, data):
        new_obj = {}
        # new_obj['id'] = raw_obj['id']
        new_obj['name'] = raw_obj['name']
        new_obj['symbol'] = raw_obj['symbol']
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
        data.append(new_obj)

    def __parse_holding_data(self, raw_obj, data):
        holdings = raw_obj['view_rebalancing']['holdings']
        if holdings:
            for holding in holdings:
                new_obj = {}
                # new_obj['id'] = raw_obj['id']
                new_obj['name'] = raw_obj['name']
                new_obj['symbol'] = raw_obj['symbol']
                new_obj['market'] = raw_obj['market']
                new_obj['created_at'] = self.__to_format_time(raw_obj['created_at'])
                new_obj['close_date'] = raw_obj['close_date']

                new_obj['weight'] = holding['weight']
                new_obj['segment_name'] = holding['segment_name']
                new_obj['stock_name'] = holding['stock_name']
                new_obj['stock_symbol'] = holding['stock_symbol']
                data.append(new_obj)

    @staticmethod
    def __to_format_time(timestamp):
        try:
            time_array = time.localtime(float(timestamp) / 1000)
            return time.strftime("%Y-%m-%d", time_array)
        except Exception:
            return ''


def draw(df):
    rows = []
    for i in range(-100, 500, 5):
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
    path = 'D:/data/'
    combiner = DataCombiner(path + '/cube_summary_sp')
    df = combiner.holding_data_df
    df.to_csv(path + '/holding_data.csv')
    df = combiner.meta_data_df
    df.to_csv(path + '/meta_data.csv')


if __name__ == '__main__':
    main()
