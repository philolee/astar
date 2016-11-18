# -*- coding=utf-8

import urllib
from urllib.request import urlopen
import ioutils
import requests
import re


session = requests.session()

def get_html(url):
    res = session.get(url)
    return res.content


def main():
    for i in range(0, 10):
        print(i, end='\r')



if __name__ == '__main__':
    main()




