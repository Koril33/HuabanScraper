import sys
import os
#得到当前根目录
o_path = os.getcwd() # 返回当前工作目录
sys.path.append(o_path)
import Scraper.HuabanScraper as HuabanScraper
import argparse

# 命令行参数
parser = argparse.ArgumentParser(description='爬取花瓣网图片')
parser.add_argument('--url', type=str, required=True, help='画板的网址')
parser.add_argument('--max', type=int, default=10, help='下载图片的最大数量（默认10张）')
parser.add_argument('--path', type=str, default='huaban_pictures', help='创建的文件夹的名字，用来保存下载图片（默认为‘huaban_pictures’）')
args = parser.parse_args()

main_page = args.url
pic_max = args.max
path_name = args.path

scraper = HuabanScraper.Scraper(main_page, pic_max, path_name)
scraper.run_and_download()

