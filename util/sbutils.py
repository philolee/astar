import datetime
import json
import re
import time

from util import ioutils

CUBE_URL = 'http://xueqiu.com/p/'
# CUBE_ID_START_POS = 100000
CUBE_ID_START_POS = 1000000


def get_cube_summary(cube_id):
    html = ioutils.get_html(CUBE_URL + cube_id)
    match = re.search('SNB.cubeInfo\s+=\s+(.+);', html)
    if match:
        data = match.group(1)
    else:
        data = ''
    return data


def get_stock_history_data(stock_id, start_time, end_time):
    url = "https://xueqiu.com/stock/forchartk/stocklist.json?symbol=%s&period=1day&type=before&begin=%d&end=%d" % (
        stock_id, start_time, end_time)
    html = ioutils.get_html(url)
    return json.loads(html)


def get_cube_id(num):
    return 'ZH%d' % num


def get_sp_cube_id(num):
    return 'SP%d' % num


def gen_file_name(start, end):
    return '%s_%s.txt' % (start, end)


def get_cube_start_pos():
    return CUBE_ID_START_POS


def get_timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())


def get_current_timestamp():
    return time.mktime(datetime.datetime.now().timetuple()) * 1000


def main():
    stock = 'SH600551'
    start = 0
    end = get_current_timestamp()
    print(start, end)

    stock_history_data = get_stock_history_data(stock, start, end)
    print(stock_history_data)


if __name__ == '__main__':
    main()
