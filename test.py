import os

def get_last_crawled_cube_id():
    files = os.listdir('/home/liyang/data/cube_summary')
    print(files)
    if len(files) != 0:
        pos = files[0].index('_')
        if pos == -1:
            print("file name error: %s", files[0])
        first = files[0][0:pos]
        return first

print(get_last_crawled_cube_id())

