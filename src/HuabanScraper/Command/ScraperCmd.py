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

parser.add_argument('-u', '--url', type=str,
                                   required=True,
                                   nargs='+',
                                   help='画板的网址')

parser.add_argument('-m', '--max', type=int,
                                   default=10,
                                   nargs='+',
                                   help='下载图片的最大数量（默认10张）')

parser.add_argument('-p', '--path', type=str,
                                    default='huaban_pictures',
                                    nargs='+',
                                    help='创建的文件夹的名字，用来保存下载图片（默认为‘huaban_pictures’）')

parser.add_argument('-f', '--filter', type=str,
                                      default='jpg/png/gif',
                                      nargs='+',
                                      help='指定下载图片格式，默认全部下载')
args = parser.parse_args()

urls = args.url
pic_max = args.max
path_name = args.path
type_filters = args.filter

for i in range(len(urls)):
    type_filter = filter_parse(type_filters[i])
    print(f'任务{i}开始下载...url:{urls[i]}, max:{pic_max[i]}, path:{path_name[i]}, type_filter:{type_filter}')
    scraper = HuabanScraper.Scraper(urls[i], pic_max[i], path_name[i], type_filter)
    scraper.run_and_download()
    print(f'-----------------任务{i}下载结束---------------------')

