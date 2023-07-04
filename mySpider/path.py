import os.path
import re
import sys

#   获取文件目录
print(os.path.abspath(os.path.dirname(__file__)))
#
print(os.path.dirname(__file__))

print(os.path.basename(__file__))

print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("sys.path[0]:" + sys.path[0])

print(os.path.dirname(sys.path[0]) + "\\douban.json")

print(os.path.dirname(os.getcwd()))

url = "https://battlecats-db.com/stage/s03000-03.html"
number_pattern = r"s(\d+)-(\d+)\.html"
match = re.search(number_pattern, url)
if match:
    number = int(match.group(2))
    print(number)  # 输出 "03"
else:
    print("未找到数字")


start_urls = [
    "https://battlecats-db.com/stage/s03000-02.html",
    "https://battlecats-db.com/stage/s03000-03.html",
    "https://battlecats-db.com/stage/s03000-04.html",
    "https://battlecats-db.com/stage/s03000-05.html",
    "https://battlecats-db.com/stage/s03000-06.html",
    "https://battlecats-db.com/stage/s03000-07.html",
    "https://battlecats-db.com/stage/s03000-08.html",
    "https://battlecats-db.com/stage/s03000-09.html",
    "https://battlecats-db.com/stage/s03000-10.html",
    "https://battlecats-db.com/stage/s03000-11.html",
    "https://battlecats-db.com/stage/s03000-12.html",
    "https://battlecats-db.com/stage/s03000-13.html",
    "https://battlecats-db.com/stage/s03000-14.html",
    "https://battlecats-db.com/stage/s03000-15.html",
    "https://battlecats-db.com/stage/s03000-16.html",
    "https://battlecats-db.com/stage/s03000-17.html",
    "https://battlecats-db.com/stage/s03000-18.html",
    "https://battlecats-db.com/stage/s03000-19.html",
    "https://battlecats-db.com/stage/s03000-20.html",
    "https://battlecats-db.com/stage/s03000-21.html",
    "https://battlecats-db.com/stage/s03000-22.html",
    "https://battlecats-db.com/stage/s03000-23.html",
    "https://battlecats-db.com/stage/s03000-24.html",
    "https://battlecats-db.com/stage/s03000-25.html",
    "https://battlecats-db.com/stage/s03000-26.html",
    "https://battlecats-db.com/stage/s03000-27.html",
    "https://battlecats-db.com/stage/s03000-28.html",
    "https://battlecats-db.com/stage/s03000-29.html",
    "https://battlecats-db.com/stage/s03000-30.html",
    "https://battlecats-db.com/stage/s03000-31.html",
    "https://battlecats-db.com/stage/s03000-32.html",
    "https://battlecats-db.com/stage/s03000-33.html",
    "https://battlecats-db.com/stage/s03000-34.html",
    "https://battlecats-db.com/stage/s03000-35.html",
    "https://battlecats-db.com/stage/s03000-36.html",
    "https://battlecats-db.com/stage/s03000-37.html",
    "https://battlecats-db.com/stage/s03000-38.html",
    "https://battlecats-db.com/stage/s03000-39.html",
    "https://battlecats-db.com/stage/s03000-40.html",
    "https://battlecats-db.com/stage/s03000-41.html",
    "https://battlecats-db.com/stage/s03000-42.html",
    "https://battlecats-db.com/stage/s03000-43.html",
    "https://battlecats-db.com/stage/s03000-44.html",
    "https://battlecats-db.com/stage/s03000-45.html",
    "https://battlecats-db.com/stage/s03000-46.html",
    "https://battlecats-db.com/stage/s03000-47.html",
    "https://battlecats-db.com/stage/s03000-48.html"
]

print(len(start_urls))
