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
