import ioutils
import re

CUBE_URL = 'http://xueqiu.com/p/'
#CUBE_ID_START_POS = 100000
CUBE_ID_START_POS = 1000000

def get_cube_summary(cube_id):
    html = ioutils.get_html(CUBE_URL + cube_id)
    match = re.search('SNB.cubeInfo\s+=\s+(.+);', html)
    if match:
        data = match.group(1)
    else:
        data = ''
    return data


def get_cube_id(num):
    return 'ZH%d' % num

def get_sp_cube_id(num):
    return 'SP%d' % num


def save_to_file(file_name, lines):
    f = open(file_name, "w")
    for line in lines:
        f.write(line + '\n')
    f.close()


def gen_file_name(start, end):
    return '%s_%s.txt' % (start, end)


def get_cube_start_pos():
    return CUBE_ID_START_POS

