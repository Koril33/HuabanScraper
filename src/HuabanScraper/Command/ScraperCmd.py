import sys
import os

o_path = os.getcwd()
sys.path.append(o_path)
import Scraper.HuabanScraper as HuabanScraper
import argparse

def filter_parse(img_filter):
    return tuple(img_filter.split('/'))

# 命令行参数
parser = argparse.ArgumentParser(description='爬取花瓣网图片')
parser.add_argument('--url', type=str, required=True, help='画板的网址')
parser.add_argument('--max', type=int, default=10, help='下载图片的最大数量（默认10张）')
parser.add_argument('--path', type=str, default='huaban_pictures', help='创建的文件夹的名字，用来保存下载图片（默认为‘huaban_pictures’）')
parser.add_argument('--filter', type=str, default='jpg/png/gif', help='指定下载图片格式，默认全部下载')
args = parser.parse_args()

main_page = args.url
pic_max = args.max
path_name = args.path
type_filter = filter_parse(args.filter)

scraper = HuabanScraper.Scraper(main_page, pic_max, path_name, type_filter)
print(type_filter)
scraper.run_and_download()

