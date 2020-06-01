import requests
import time
import concurrent.futures


class DownloadPic:
    def __init__(self):
        self.__download_count = 0

    def download_image(self, img_url, path_name, img_name):
        """下载单张图片
        :param img_url: 下载图片的地址
        :param path_name: 下载图片到指定的文件夹
        :param img:
        """

        r = requests.get(img_url)

        if not '/' in path_name:
            path_name = './' + path_name

        with open(f'{path_name}/{img_name}.png', 'wb') as image_file:
            image_file.write(r.content)
        self.__download_count += 1
        print(
            f'image_{img_name} is downloaded! count : {self.__download_count}')

    def download_all_by_urls(self, img_urls, path_name):
        """多线程下载
        :param img_urls: 所有图片的下载地址
        :param path_name: 下载图片到指定的文件夹
        """
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for index, image_url in enumerate(img_urls):
                executor.submit(self.download_image,
                                image_url, path_name, index)

        print(f'It spends {time.time() - start_time} seconds')
