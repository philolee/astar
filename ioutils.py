# -*- coding=utf-8

import urllib
from urllib.request import urlopen
import zlib

def get_html(url):
    send_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Cache-Control': 'max-age=0',
        'Cookie': 'webp=1; bid=7247918f8c2d763975843abc0f65f2e1_iui0zl7q; __utma=1.2059918714.1477908998.1479291064.1479376597.3; __utmc=1; __utmz=1.1477908998.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); s=7w12lut23p; last_account=philo_ly%40163.com; xq_a_token=e8e54f45363e45c762c42cd926e470175c1123a1; xq_r_token=36c71dba39380a7c439676ea63f63f717faa677b; Hm_lvt_1db88642e346389874251b5a1eded6e3=1478859231,1479195244,1479363316,1479448630; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1479459758',
        'Host': 'xueqiu.com'
    }
    try:
        req = urllib.request.Request(url, headers=send_headers)
        resp = urlopen(req)
        if resp.info().get('Content-Encoding') == 'gzip':
            html = zlib.decompress(resp.read(), 16+zlib.MAX_WBITS)
            html = html.decode('utf-8')
        else:
            html = resp.read().decode(resp.headers.get_content_charset())
    except Exception as e:
        print('request failed, url:', url, 'error:', e)
        html = ''
    return html


def write_lines_to_file(file_name, lines):
    f = open(file_name, "w", encoding='utf-8')
    for line in lines:
        f.write(line + '\n')
    f.close()