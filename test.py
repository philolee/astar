# -*- coding=utf-8

import requests
import datetime

session = requests.session()

def get_html(url):
    res = session.get(url)
    return res.content


def main():
    timestr = '2016-11-01'
    date = datetime.datetime.strptime(timestr, '%Y-%m-%d')
    date = date + datetime.timedelta(days=-365)
    print(date)



if __name__ == '__main__':
    main()




