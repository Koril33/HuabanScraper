import json
import os
import requests
import sys
import concurrent.futures
import time
import argparse

# 命令行参数
parser = argparse.ArgumentParser(description='爬取花瓣网图片')
parser.add_argument('--url', type=str, required=True, help='画板的网址')
parser.add_argument('--max', type=int, default=10, help='下载图片的最大数量（默认10张）')
parser.add_argument('--path', type=str, default='huaban_pictures',
                    help='创建的文件夹的名字，用来保存下载图片（默认为‘huaban_pictures’）')
args = parser.parse_args()

main_page = args.url
pic_max = args.max
path_name = args.path

# 测试使用的网站
# main_page = 'https://huaban.com/discovery/beauty/'
# main_page = 'https://huaban.com/explore/manhuarenwu'
# main_page = 'https://huaban.com/boards/37776086/'
# main_page = 'https://huaban.com/favorite/design/'

# 构造请求头
my_header = {
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


def create_url_l(url):
    """构造页面url的左半部分
    :param url: 用户传入的url
    :return: 构造后的url
    """

    if url.endswith('/'):
        return url + '?&max='
    else:
        return url.split('/?', maxsplit=1)[0] + '/?&max='


# 图片下载url，左半部分为定值
pic_url_l = 'http://img.hb.aicdn.com/'
# 页面url左半部分，通过create_url_l函数构造
page_url_l = create_url_l(main_page)
# 页面url右半部分
page_url_r = '&limit=20&wfl=1'
# 所有图片的下载地址
all_urls = []


def is_board_or_discovery(url):
    """判断下载的页面是画板（board）还是发现（discovery）
    一般'board'以数字结尾，'discovery'以字母结尾
    :param url: 用户传入的url
    :return: 返回标志
    """

    tag = url.split('/')[-2]
    if tag.isdigit():
        return 'board'
    else:
        return 'discovery'


# 判断是画板还是发现的标志
is_board_or_discovery_tag = is_board_or_discovery(main_page)


def get_first_page_urls(url, tag):
    """下载时，第一页和其它页分开
    此函数获取第一页图片的下载地址
    :param url: 第一页url
    :param tag: board还是discovery
    :return: 第一页最后一张图片的id
    """
    # 请求json数据
    first_page_response = requests.get(url, headers=my_header)
    first_page_response.encoding = 'utf-8'
    first_page_json_result = first_page_response.json()

    # 画板和发现的json格式不一样，需要分开处理
    if tag == 'discovery':
        first_page_pins = first_page_json_result['pins']
    elif tag == 'board':
        first_page_pins = first_page_json_result['board']['pins']

    for i in range(len(first_page_pins)):
        # 获取图片真实下载地址，并添加到all_urls中
        url = pic_url_l + first_page_pins[i]['file']['key']
        all_urls.append(url)

        # 如果超过用户指定的max值，则结束
        if len(all_urls) >= pic_max:
            return

    first_page_next_url_id = first_page_pins[-1]['pin_id']

    return first_page_next_url_id


def get_all_urls(url, tag):
    """下载时，第一页和其它页分开
    此函数获取所有页面图片的下载地址
    :param url: 下一页的url
    :param tag: board还是discovery
    """

    # 当页面超过一页时，先下载第一页，并获得第一页最后的id值
    first_page_next_url_id = get_first_page_urls(url, tag)

    # print(first_page_next_url_id)

    url = create_next_request_url(first_page_next_url_id)

    # print(url)
    while True:
        # 请求json数据
        response = requests.get(url, headers=my_header)
        response.encoding = 'utf-8'
        json_result = response.json()

        # 画板和发现的json格式不一样，需要分开处理
        if tag == 'discovery':
            pins = json_result['pins']
        elif tag == 'board':
            pins = json_result['board']['pins']

        for i in range(len(pins)):
            # 获取图片真实下载地址，并添加到all_urls中
            url = pic_url_l + pins[i]['file']['key']
            all_urls.append(url)

            # 如果超过用户指定的max值，则结束
            if len(all_urls) >= pic_max:
                return

        # 如果用户给的max值超过当前页面的图片数量，会抛出IndexError
        try:
            next_url_id = pins[-1]['pin_id']
        except IndexError:
            print('指定的pic_max值超过画板图片总数！')
            return

        # 获取下一页的url
        next_page_url = create_next_request_url(next_url_id)
        url = next_page_url


def create_next_request_url(id_num):
    """构造下一页的url
    :param id_num: 每个页面url都有个独特的max值（上一页最后一张图片的id_num）
    :return: 下一页的url
    """

    return page_url_l + str(id_num) + page_url_r


def download_image(img_url, path_name, img_name):
    """下载单张图片
    :param img_url: 下载图片的地址
    :param path_name: 下载图片到指定的文件夹
    :param img:
    """

    r = requests.get(img_url)
    with open(f'./{path_name}/{img_name}.png', 'wb') as image_file:
        image_file.write(r.content)
    print(f'image_{img_name} is downloaded!')


def download_all_by_urls(img_urls, path_name):
    """多线程下载
    :param img_urls: 所有图片的下载地址
    :param path_name: 下载图片到指定的文件夹
    """
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, image_url in enumerate(img_urls):
            executor.submit(download_image, image_url, path_name, index)

    print(f'It spends {time.time() - start_time} seconds')


def main():
    """主函数
    """

    if pic_max <= 20:
        get_first_page_urls(url=main_page, tag=is_board_or_discovery_tag)
    else:
        get_all_urls(url=main_page, tag=is_board_or_discovery_tag)

    # 创建文件夹
    if not os.path.exists(path_name):
        os.mkdir(path_name)
    else:
        print(f'{path_name} exists!')

    # 多线程下载
    download_all_by_urls(all_urls, path_name)

    # 打印图片总数
    print(f'total: {len(all_urls)}')


if __name__ == '__main__':
    main()
