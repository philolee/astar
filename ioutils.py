import urllib
from urllib.request import urlopen


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


def write_lines_to_file(file_name, lines):
    f = open(file_name, "w", encoding='utf-8')
    for line in lines:
        f.write(line + '\n')
    f.close()