import requests
import time
import concurrent.futures


class DownloadPic:
    def __init__(self):
        self.__download_count = 0

    def download_image(self, img_url, path_name, img_name, raw_type):
        """下载单张图片
        :param img_url: 下载图片的地址
        :param path_name: 下载图片到指定的文件夹
        :param img:
        """

        r = requests.get(img_url)

        if not '/' in path_name:
            path_name = './' + path_name

        download_type = self.create_download_type(raw_type)

        with open(f'{path_name}/{img_name}.{download_type}', 'wb') as image_file:
            image_file.write(r.content)
        self.__download_count += 1
        print(
            f'image_{img_name} is downloaded! count : {self.__download_count}')

    def download_all_by_urls(self, img_urls, path_name):
        """多线程下载
        :param img_urls: 所有图片的下载地址以及下载格式
        :param path_name: 下载图片到指定的文件夹
        """
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for index, image_url in enumerate(img_urls):
                executor.submit(self.download_image,
                                    image_url, 
                                    path_name, 
                                    index, 
                                    img_urls[image_url]['img_type'])

        print(f'It spends {time.time() - start_time} seconds')

    def get_download_count(self):
        '''getter __download_count
        '''

        return self.__download_count

    def create_download_type(self, raw_type):
        if raw_type == 'image/jpeg':
            return 'jpg'
        elif raw_type == 'image/gif':
            return 'gif'
        else:
            return 'png'