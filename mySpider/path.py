import os.path
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