import pandas as pd
import os
import datetime
from util import sbutils


class MainFlow:
    input_path = ''
    stock_names = []

    def __init__(self, input_path=None):
        self.input_path = input_path
        self.stock_names = os.listdir(input_path)

    def __get_stock_df(self, stock_name):
        if stock_name.find('SZ') == -1 and stock_name.find('SH') == -1:
            stock_name = sbutils.get_stock_name(stock_name)

        if stock_name.find('.csv') == -1:
            return pd.read_csv(self.input_path + stock_name + '.csv')
        else:
            return pd.read_csv(self.input_path + stock_name)

    def n_dats_ago(self, timestr, n):
        date = datetime.datetime.strptime(timestr, '%Y-%m-%d')
        date = date + datetime.timedelta(days=-n)
        return date.strftime('%Y-%m-%d')

    def process(self, stocks, begin_date, end_date):
        """
        获取待选个股
        获取起始时间
        循环每一天
            是否买入
            是否卖出
            计算基本收益
        """
        # filter stock_names
        days_after = 200
        if stocks:
            self.stock_names = stocks
        data = []
        for stock in self.stock_names:
            stock_history = self.__get_stock_df(stock)
            try:
                stock_history = stock_history[(stock_history.date >= begin_date) & (stock_history.date <= end_date)]
            except Exception:
                print(stock)
            count = 0
            max_price = 0
            account = Account()
            last_stock_meta = None
            for row in stock_history.itertuples():
                if count < days_after:
                    if max_price < row.close:
                        max_price = row.close
                    count += 1
                    continue

                if account.amount > 1000 and row.close > max_price:
                    account.buy_all(stock, row)
                if account.amount != 100000 and row.close < row.ma20:
                    account.sell_all(stock, row)
                    break
                last_stock_meta = row
            if account.amount < 1000:
                account.sell_all(stock, last_stock_meta)
            ret = account.print_gain_detail()
            if len(ret) > 0:
                data.append(ret)
        return data


class Account:
    amount = 100000
    holdings = {}
    rebalance_history = []
    detail = {}

    def __init__(self):
        self.holdings = {}
        self.rebalance_history = []
        self.detail = {}

    def buy_all(self, stock_name, stock_meta):
        volume = self.amount / stock_meta.close
        self.amount -= volume * stock_meta.close
        buy_detail = {'date': stock_meta.date, 'close': stock_meta.close, 'volume': volume}
        self.holdings[stock_name] = buy_detail
        self.rebalance_history.append('date: %s, buy: %s, price:%d' % (stock_meta.date, stock_name, stock_meta.close))
        self.detail['stock'] = stock_name
        self.detail['buy_date'] = stock_meta.date
        self.detail['buy_price'] = stock_meta.close

    def sell_all(self, stock_name, stock_meta):
        if stock_name in self.holdings.keys():
            buy_detail = self.holdings[stock_name]
            self.amount += stock_meta.close * buy_detail['volume']
            self.rebalance_history.append(
                'date: %s, sell: %s, price:%d' % (stock_meta.date, stock_name, stock_meta.close))
            del self.holdings[stock_name]
            self.detail['sell_date'] = stock_meta.date
            self.detail['sell_price'] = stock_meta.close

    def print_gain_detail(self):
        if len(self.rebalance_history) != 0:
            print("#####################################################")
            for rebalance in self.rebalance_history:
                print(rebalance)
            gain = 100 * (self.amount - 100000) / 100000
            print('total gain: %.2f' % (100 * (self.amount - 100000) / 100000))
            print("#####################################################")
            self.detail['gain'] = gain
            return self.detail
        return []


if __name__ == '__main__':
    input_path = 'D:/data/stock_history_df/'
    stocks = ['SZ000935']
    main_flow = MainFlow(input_path)

    data = main_flow.process(None, '2015-08-01', '2016-11-17')
    df = pd.DataFrame(data, columns=['stock', 'buy_date', 'sell_date', 'buy_price', 'sell_price', 'gain'])
    df.to_csv('D:/data/new_high.csv')
    print('done')
