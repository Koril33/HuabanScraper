import json
import os
import requests
import sys
import concurrent.futures
import time

import sys
import os
o_path = os.getcwd()
sys.path.append(o_path)
import Utils.DownloadUtil as DownloadUtil
import Utils.MakeDir as MakeDir

class Scraper:
    def __init__(self, main_page, pic_max, path_name, type_filter=('jpg', 'png', 'gif')):
        self.__main_page = main_page
        self.__pic_max = int(pic_max)
        self.__path_name = path_name
        # 图片下载url，左半部分为定值
        # self.__pic_url_l = 'https://hbimg.huabanimg.com/'
        self.__pic_url_l = 'http://img.hb.aicdn.com/'
        # 页面url左半部分，通过create_url_l函数构造
        self.__page_url_l = self.create_url_l(self.__main_page)
        # 页面url右半部分
        self.__page_url_r = '&limit=20&wfl=1'
        # 所有图片的下载地址和图片类型
        self.__all_urls = {}
        # 判断是画板还是发现的标志
        self.__tag = self.create_tag(self.__main_page)
        # 已经下载的图片数量，用来显示进度条
        self.__download_count = 0
        # 指定下载数量是否超出图片总数
        self.__overtax = False

        # 下载的对象
        self.download = DownloadUtil.DownloadPic()

        # 过滤的类型
        self.__type_filter = type_filter

        # 构造请求头
        self.__my_header = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'huaban.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'X-Request': 'JSON',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def create_url_l(self, url):
        """构造页面url的左半部分
        :param url: 用户传入的url
        :return: 构造后的url
        """

        if url.endswith('/'):
            return url + '?&max='
        else:
            return url.split('/?', maxsplit=1)[0] + '/?&max='

    def create_tag(self, url):
        """判断下载的页面类型
                'https://huaban.com/discovery/geek/',
                'https://huaban.com/boards/43427316/',
                'https://huaban.com/pins/3083753516/',
        一般'board'以数字结尾，'discovery'以字母结尾
        :param url: 用户传入的url
        :return: 返回标志
        """

        tags = {'discovery', 'boards', 'pins', 'explore', 'favorite'}
        try:
            tag = url.split('/')[3]
            if tag in tags:
                return tag
            else:
                return 'error'
        except:
            print('url has mistake!')
            return 'error'

    def create_pins(self, json_data, tag):
        """通过tag来获取json的数据
        :param json_data: get得到的json
        :param tag: 页面标签
        :return: pins的字典
        """

        if tag == 'discovery':
            pins = json_data['pins']
            return pins
        elif tag == 'boards':
            pins = json_data['board']['pins']
            return pins
        elif tag == 'explore':
            pins = json_data['pins']
            return pins
        elif tag == 'favorite':
            pins = json_data['pins']
            return pins
        elif tag == 'pins':
            self.__all_urls[self.__pic_url_l
                                   + json_data['pin']['file']['key']] = {'img_type' : json_data['pin']['file']['type']}
            return 'single_pic'
        else:
            return

    def create_first_page_urls(self, url, tag):
        """下载时，第一页和其它页分开
        此函数获取第一页图片的下载地址
        :param url: 第一页url
        :param tag: board还是discovery
        :return: 第一页最后一张图片的id
        """

        # 请求json数据
        try:
            first_page_response = requests.get(url, headers=self.__my_header)
        except:
            return
        first_page_response.encoding = 'utf-8'
        first_page_json_result = first_page_response.json()

        # 画板和发现的json格式不一样，需要分开处理
        first_page_pins = self.create_pins(first_page_json_result, tag)

        if first_page_pins == 'single_pic':
            print('下载单张pin图')
            return
        elif first_page_pins is None:
            print('不支持此tag')
            return

        for i in range(len(first_page_pins)):
            # 获取图片真实下载地址，并添加到all_urls中
            img_type = self.download.create_download_type(first_page_pins[i]['file']['type'])
            if img_type in self.__type_filter:
                url = self.__pic_url_l + first_page_pins[i]['file']['key']
                self.__all_urls[url] = {'img_type' : first_page_pins[i]['file']['type']}

            # 如果超过用户指定的max值，则结束
            if len(self.__all_urls) >= self.__pic_max:
                return

        first_page_next_url_id = first_page_pins[-1]['pin_id']

        return first_page_next_url_id

    def create_all_urls(self, url, tag):
        """下载时，第一页和其它页分开
        此函数获取所有页面图片的下载地址
        :param url: 下一页的url
        :param tag: board还是discovery
        """

        # 当页面超过一页时，先下载第一页，并获得第一页最后的id值
        first_page_next_url_id = self.create_first_page_urls(url, tag)

        # if len(self.__all_urls) < 20:
        #     self.__overtax = True
        #     return

        if first_page_next_url_id is None:
            pass
        elif first_page_next_url_id == 'single_pic':
            return
        # print(first_page_next_url_id)

        url = self.create_next_request_url(first_page_next_url_id)

        # print(url)
        while True:
            # 请求json数据
            response = requests.get(url, headers=self.__my_header)
            response.encoding = 'utf-8'
            json_result = response.json()

            # 画板和发现的json格式不一样，需要分开处理
            pins = self.create_pins(json_result, tag)
            
            if pins == 'single_pic':
                print('下载单张pin图')
                return
            elif pins is None:
                print('不支持此tag')
                return

            for i in range(len(pins)):
                # 获取图片真实下载地址，并添加到all_urls中
                img_type = self.download.create_download_type(pins[i]['file']['type'])
                if  img_type in self.__type_filter:
                    url = self.__pic_url_l + pins[i]['file']['key']
                    self.__all_urls[url] = {'img_type' : pins[i]['file']['type']}

                # 如果超过用户指定的max值，则结束
                if len(self.__all_urls) >= self.__pic_max:
                    print('len: ', len(self.__all_urls))
                    return

            # 如果用户给的max值超过当前页面的图片数量，会抛出IndexError
            try:
                next_url_id = pins[-1]['pin_id']
            except IndexError:
                print('指定的pic_max值超过画板图片总数！')
                self.__overtax = True
                return

            # 获取下一页的url
            next_page_url = self.create_next_request_url(next_url_id)
            url = next_page_url

    def create_next_request_url(self, id_num):
        """构造下一页的url
        :param id_num: 每个页面url都有个独特的max值（上一页最后一张图片的id_num）
        :return: 下一页的url
        """

        return self.__page_url_l + str(id_num) + self.__page_url_r

    def get_all_urls(self):
        '''getter __all_urls
        '''

        return self.__all_urls

    def get_overtax_flag(self):
        return self.__overtax

    def run_and_download(self):
        """获取所有url并下载
        """

        if self.__pic_max <= 20:
            self.create_first_page_urls(
                url=self.__main_page, tag=self.__tag)
        else:
            self.create_all_urls(url=self.__main_page,
                                 tag=self.__tag)

        # 创建文件夹
        MakeDir.make_download_dir(self.__path_name)

        # 多线程下载
        self.download.download_all_by_urls(self.__all_urls, self.__path_name)

        # 打印图片总数
        print(f'total: {len(self.__all_urls)}')

    def run_without_download(self):
        '''获取所有url但不下载
        '''

        if self.__pic_max <= 20:
            self.create_first_page_urls(
                url=self.__main_page, tag=self.__tag)
        else:
            self.create_all_urls(url=self.__main_page,
                                 tag=self.__tag)


if __name__ == '__main__':
    urls_test = [
        'https://huaban.com/discovery/geek/',
        'https://huaban.com/boards/43427316/',
        'https://huaban.com/pins/3083753516/',
        'https://huaban.com/favorite/beauty/',
    ]

    scraper_list = []
    download_num = 30
    type_filter = ('png', )
    for i in range(len(urls_test)):
        scraper = Scraper(urls_test[i], download_num, f'测试{i}')
        scraper_list.append(scraper)

    for scraper in scraper_list:
        scraper.run_and_download()
        # scraper.run_without_download()
        # for index, img_url in enumerate(scraper.get_all_urls()):
        #     print(f'index:{index}, url:{img_url}, type:{scraper.get_all_urls()[img_url]["img_type"]}')
    