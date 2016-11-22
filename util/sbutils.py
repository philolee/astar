import datetime
import re
import time

from util import ioutils

CUBE_URL = 'http://xueqiu.com/p/'


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
    return html


def get_cube_id(num):
    return 'ZH%d' % num


def get_sp_cube_id(num):
    return 'SP%d' % num


def get_stock_name(id):
    if id > 600000:
        return 'SH%d' % id
    return 'SZ%06d' % id


def gen_file_name(start, end):
    return '%s_%s.txt' % (start, end)


def get_timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())


def get_current_timestamp():
    return time.mktime(datetime.datetime.now().timetuple()) * 1000


def main():
    print(get_stock_name(2202))


if __name__ == '__main__':
    main()
