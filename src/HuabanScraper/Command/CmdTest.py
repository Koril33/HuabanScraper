import sys
import os
o_path = os.getcwd()
sys.path.append(o_path)
import Scraper.HuabanScraper as HuabanScraper
from multiprocessing import Pool
import multiprocessing
import configparser

config_file = 'config.ini'
con = configparser.ConfigParser()
con.read(config_file, encoding='utf-8')
section = con.sections()

num = len(section)

urls = []
pic_max = []
path_name = []
type_filters = []

for i in range(num):
    item = con.items(f'url{i+1}')
    urls.append(item[0][1])
    pic_max.append(item[1][1])
    path_name.append(item[2][1])
    type_filters.append(item[3][1])

def filter_parse(img_filter):
    return tuple(img_filter.split('/'))


def download_all(i, url, pic_max, path_name, type_filter):
    
        type_filter = filter_parse(type_filter)
        print(f'任务{i}开始下载...url:{url}, max:{pic_max}, path:{path_name}, type_filter:{type_filter}')
        scraper = HuabanScraper.Scraper(url, pic_max, path_name, type_filter)
        scraper.run_and_download()
        print(f'-----------------任务{i}下载结束---------------------')


def main():

    p = Pool(4)
    for i in range(len(urls)):
        ret = p.apply_async(download_all,args=(i, urls[i], pic_max[i], path_name[i], type_filters[i]))  # 异步的，一个运行完才执行另一个
    p.close()
    p.join()
        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()