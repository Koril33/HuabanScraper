import requests
import re
import time
import os
from pixivpy3 import *

api = AppPixivAPI()
api.login("dingjinghui33@163.com", "159756")   # Not required

img_list = []
json_result = api.user_illusts(843975)
print(json_result)
pins = json_result['illusts']
print('length: ', len(pins))
for pin in pins:
    img_url = pin['image_urls']['large']
    print(img_url)
    img_list.append(img_url)
    # img_id = pin['id']
    # print(img_id)

my_header = {
    'Host': 'www.pixiv.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.pixiv.net/users/27517/illustrations?p=1',
    'Connection': 'keep-alive',
    'Cookie': '__cfduid=deae6694b5b6d0f50403e5a49daa0b2881591159550; first_visit_datetime_pc=2020-06-03+13%3A45%3A50; PHPSESSID=rd3buqrpo26am3i5mh410rd1aee05lao; p_ab_id=5; p_ab_id_2=8; p_ab_d_id=428808859; __utma=235335808.2087472645.1591159551.1591159551.1591159551.1; __utmb=235335808.6.10.1591159551; __utmc=235335808; __utmz=235335808.1591159551.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|3=plan=normal=1^11=lang=zh=1; yuid_b=JlKHiZg; __utmt=1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
}


def download_image(img_url, path_name, img_name):
        """下载单张图片
        :param img_url: 下载图片的地址
        :param path_name: 下载图片到指定的文件夹
        :param img:
        """

        r = requests.get(img_url, headers=my_header)

        if not '/' in path_name:
            path_name = './' + path_name

        make_download_dir(path_name)

        # download_type = img_url.rsplit('.', maxsplit = 1)[-1]
        download_type = 'png'

        with open(f'{path_name}/{img_name}.{download_type}', 'wb') as image_file:
            image_file.write(r.content)
        
        print(f'image_{img_name} is downloaded! ')


def make_download_dir(path_name):
    '''创建下载图片的文件夹
    :param path: 文件夹名字
    '''

    if not os.path.exists(path_name):
        os.mkdir(path_name)
    else:
        print(f'{path_name} exists!')

# tmp = [
#     'https://i.pximg.net/img-original/img/2020/05/31/00/15/09/81974549_p0.png',
#     'https://i.pximg.net/img-original/img/2020/04/01/00/03/22/80481527_p0.png',
#     'https://i.pximg.net/img-original/img/2020/04/04/00/10/00/80545109_p0.png',
# ]
def main():
    for index, img in enumerate(img_list):
        try:
            # img_url = img['src']
            s = re.search('img/.*_p0', img).group(0)
            # result = 'https://i.pximg.net/img-original/' + s + '.' + img_url.rsplit('.', maxsplit = 1)[-1]
            result = 'https://i.pximg.net/img-original/' + s + '.' + 'jpg'
            print(f'url: {result} index: {index}')
        
            download_image(result, '测试', str(index))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()


