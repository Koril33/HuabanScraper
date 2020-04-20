from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import time
import re
import concurrent.futures

# 画板的url地址
first_url = 'https://huaban.com/boards/58520585/'
# 保存图片的本地文件夹名字
path_name = 'pictures_test_test'
# 指定最多下载的数量
pic_max = 500

# 用正则提取url中的id值
# user_id = re.findall(r'(?:/)(\d+)(?:/)', first_url)[0]
# 每一个网页url，左半部分的固定值
# url_l = f'https://huaban.com/boards/{user_id}/?&max='
url_l = first_url + '?&max='
# url_l = first_url.split('=', 1)[0] + '='
# 每一个网页url，右半部分的固定值
url_r = '&limit=20&wfl=1'
# 单张图片url左边的固定值
page_url = 'https://huaban.com/pins/'

driver = webdriver.Firefox()

# 存放所有图片的下载地址
all_urls = []

# 登陆flag，未登录为False,登陆后改成True
login_flag = False

# 找到本页20个图片的id值，构造下载地址，保存到all_urls中
# 同时返回最后一个图片id值，用来构造下一页url
# 如果没有下一个图片id值，返回False，说明到达最后一页
# 超过指定的数量，返回False，说明下载数量已达到指定数量
def find_page_pic_urls(page_url):
    driver.get(page_url)
    # 模拟登录
    global login_flag
    if not login_flag:    
        login(driver)
        # 登陆成功后将login_flag改为True
        login_flag = True
    # 获取BeautifulSoup对象
    bs = BeautifulSoup(driver.page_source, 'lxml')
    # 找到当前页面所有的缩略图的href
    img_pic_list = bs.find_all('a', {'class':'img x layer-view loaded'})
    pic_nums = []
    for img in img_pic_list:
        # 从缩略图中的href提取图片id
        pic_num = re.findall(r'(?:/)(\d+)(?:/)', img['href'])[0]
        pic_nums.append(pic_num)
        
    for pic_num in pic_nums:
        download_url = create_download_url(pic_num)
        if download_url != None:
            all_urls.append(download_url)
        print(f'已获取第 {len(all_urls)} 张图片')
        if len(all_urls) >= pic_max:
            return False
    try:
        next_page_num = pic_nums.pop()
        return next_page_num
    except:
        return False

# 构造单张图片下载地址
def create_download_url(pic_num):
    page = page_url + pic_num
    driver.get(page)
    src = driver.page_source
    bs = BeautifulSoup(src, 'lxml')
    download_url = ''
    try:
        download_url = bs.find('div', {'class':'image-holder'}).img['src']
    except:
        pass
    if download_url == '':
        return None
    else:
        return 'http:'+download_url

# 根据上一页最后一张图片id值，构造下一张网页的url
def create_next_page_url(next_pic_num):
    return url_l + next_pic_num + url_r

# 循环，直到找到最后一页，有点像遍历单链表
def find_all_pic_urls(first_url):
    current_page = first_url
    while True:
        next_page_num = find_page_pic_urls(current_page)
        if not next_page_num:
            break
        else:
            current_page = create_next_page_url(next_page_num)


# 下载单张图片到指定路径
def download_image(image_url, path_name, img_name):
    r = requests.get(image_url)
    with open(f'./{path_name}/{img_name}.png', 'wb') as image_file:
        image_file.write(r.content)
    print(f'image_{img_name} is downloaded!')

# 根据url列表，开启多线程下载
def download_all_by_urls(image_urls, path_name):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, image_url in enumerate(image_urls):
            executor.submit(download_image, image_url, path_name, index)

    print(f'It spends {time.time() - start_time} seconds')


# 模拟登录
def login(driver):
    user_name = '你的账户'
    password = '你的密码'
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div[3]/a/span').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/div[2]/div/form/input[2]').clear()
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/div[2]/div/form/input[2]').send_keys(user_name)
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/div[2]/div/form/input[3]').clear()
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/div[2]/div/form/input[3]').send_keys(password)
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/div[2]/div/form/a').click()


# 主函数
def main():
    # 找到所有图片的下载地址，保存到all_urls列表中
    find_all_pic_urls(first_url)

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