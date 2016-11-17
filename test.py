import urllib
import json
import re
from urllib.request import urlopen
import pandas as pd
import numpy as np


def get_html(url):
    send_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'xueqiu.com',
        'Cookie': r'xxxxxx',
    }
    req = urllib.request.Request(url, headers=send_headers)
    resp = urlopen(req)
    html = resp.read().decode(resp.headers.get_content_charset())
    return html



mainURL = 'http://xueqiu.com/p/'

cubeId = 'ZH100061'

html = get_html(mainURL + cubeId)
match = re.search('SNB.cubeInfo\s+=\s+(.+);', html)
if match:
    data = match.group(1)
#pos_start = html.find('SNB.cubeInfo = ') + 15
#pos_end = html.find('SNB.cubePieData') - 2
#data = html[pos_start:pos_end]
dic = json.loads(data)

print(dic)

