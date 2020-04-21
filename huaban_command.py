import json
import os
import requests
import sys
import concurrent.futures
import time
import argparse


parser = argparse.ArgumentParser(description='爬取花瓣网图片')
parser.add_argument('--url', type=str, required=True, help='画板的网址')
parser.add_argument('--max', type=int, default=10, help='下载图片的最大数量（默认10张）')
parser.add_argument('--path', type=str, default='huaban_pictures',
                    help='创建的文件夹的名字，用来保存下载图片（默认为‘huaban_pictures’）')
args = parser.parse_args()

main_page = args.url
pic_max = args.max
path_name = args.path



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
    if url.endswith('/'):
        return url + '?&max='
    else:
        return url.split('/?', maxsplit=1)[0] + '/?&max='


pic_url_l = 'http://img.hb.aicdn.com/'

page_url_l = create_url_l(main_page)

page_url_r = '&limit=20&wfl=1'

all_urls = []


def is_board_or_discovery(url):

    tag = url.split('/')[-2]
    if tag.isdigit():
        return 'board'
    else:
        return 'discovery'


is_board_or_discovery_tag = is_board_or_discovery(main_page)


def get_first_page_urls(url, tag):

    first_page_response = requests.get(url, headers=my_header)
    first_page_response.encoding = 'utf-8'
    first_page_json_result = first_page_response.json()

    if tag == 'discovery':
        first_page_pins = first_page_json_result['pins']
    elif tag == 'board':
        first_page_pins = first_page_json_result['board']['pins']

    for i in range(len(first_page_pins)):

        url = pic_url_l + first_page_pins[i]['file']['key']
        all_urls.append(url)

        if len(all_urls) >= pic_max:
            return

    first_page_next_url_id = first_page_pins[-1]['pin_id']

    return first_page_next_url_id


def get_all_urls(url, tag):

    first_page_next_url_id = get_first_page_urls(url, tag)

    url = create_next_request_url(first_page_next_url_id)

    while True:

        response = requests.get(url, headers=my_header)
        response.encoding = 'utf-8'
        json_result = response.json()

        if tag == 'discovery':
            pins = json_result['pins']
        elif tag == 'board':
            pins = json_result['board']['pins']

        for i in range(len(pins)):

            url = pic_url_l + pins[i]['file']['key']
            all_urls.append(url)

            if len(all_urls) >= pic_max:
                return

        try:
            next_url_id = pins[-1]['pin_id']
        except IndexError:
            print('指定的pic_max值超过画板图片总数！')
            return

        next_page_url = create_next_request_url(next_url_id)
        url = next_page_url


def create_next_request_url(id_num):

    return page_url_l + str(id_num) + page_url_r


def download_image(img_url, path_name, img_name):

    r = requests.get(img_url)
    with open(f'./{path_name}/{img_name}.png', 'wb') as image_file:
        image_file.write(r.content)
    print(f'image_{img_name} is downloaded!')


def download_all_by_urls(img_urls, path_name):

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, image_url in enumerate(img_urls):
            executor.submit(download_image, image_url, path_name, index)

    print(f'It spends {time.time() - start_time} seconds')


def main():

    if pic_max <= 20:
        get_first_page_urls(url=main_page, tag=is_board_or_discovery_tag)
    else:
        get_all_urls(url=main_page, tag=is_board_or_discovery_tag)

    if not os.path.exists(path_name):
        os.mkdir(path_name)
    else:
        print(f'{path_name} exists!')

    download_all_by_urls(all_urls, path_name)

    print(f'total: {len(all_urls)}')


if __name__ == '__main__':
    main()
