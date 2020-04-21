import json
import os
import requests
import sys
import concurrent.futures
import time


# main_page = 'https://huaban.com/discovery/beauty/?k997zx3r&max=3104931188&limit=20&wfl=1'
main_page = 'https://huaban.com/discovery/beauty/'

# main_page = 'https://huaban.com/boards/60315823/'

# main_page = 'https://huaban.com/discovery/men/'


my_header = {
	'Accept': 'application/json',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Connection': 'keep-alive',
	'Cookie': r'referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIRFOJ3VwYrQCv8MsDMZBtQRcH-W9maj4u8dkXhlzT73%26wd%3D%26eqid%3Dbb4ab9a600001501000000045e9bbb83; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAACuUlEQVRYR%2B2WT0gUURzHP88gQkXpkAShFkKQGQQ6hRTMGBGR0S0PQlKQRIdYkyDr0MGLHoJcurUdysBDEUGURVQ7S0Hk6iFIiyDJhBALIYhFCvfFb3YW1nV3HHVWEprTg%2Fed976f378ZhdYar0cp5bm%2FSpt9M32ePpWAFCcSRNrbHUuhcJhwKOSs2yMREiUlniAaioEIcENBrFBcvkDkcjOW8hAzzXlrfGREww5AiIf%2FOZANs7O09ffTOjBgAaPAbeACMOFmoBUYkMQB1UAjcAWYAo4CiRw62S8DjqR1Cn74gV9SRmxLPKcey7aZrqhgrLbWkEhrOA68BypkX8pIpwwNAZuAcy6okWnMQ9cs5yn4EDhIdmnlAfkOPAL2Am%2Fd6AuIU1pumdUB0Ty6OgX30oFZTZAW9%2BLLwANATEpmpMSkVK66GUkbNN0IS%2Ba8dE6GAwXJnFqXenq429LC55oaunp7%2BVpVJVGX6D8F3gFPANsFGQTKgW7gFHAxo2%2BkxLJ10j%2F7gJPALdlX0BVoaeU9zMfU8mNkpRrfzf4fZKWh9vl%2BQTKiYyMH0HP9jge1rg2tr0OyXNbKrH%2BZ7U3bw6Oga0GNKathZz7vXrpsEPPbNsbLZpgs%2FZmysdx%2FLW0PdYParSzjmLbj553DLOPaQghH16wso17b8RHQj5W1R6bdvMc9L68uDVL5q5xDk9udd59VfgoCJH4CxRllGvt1dLiPIvUwZzZi8eck%2BaKajNM6Gr9JEVuVaRxcALKILjMjAtM4Vc2bzRMrBxEjOhZ%2FjeY%2BWlWrpoaOXCWj1wSIRFg5%2F1mDucrKhV0DGUn1yVmgU1nGnZwZSWkC6xG5owClJdMr2SEN7zVFs6eR0ytKH86ecl668K5XL9IQ0uylf9bzu2iO6JZxPm6cXv7U8jn%2BA5MV5DsSmLslHLQYyF%2BE5uEo80zUAQAAAABJRU5ErkJggg%3D%3D%2CWin32.1536.864.24; _uab_collina=158726444270333811057022; UM_distinctid=171905551f170b-04594c7ad502da-5313f6f-144000-171905551f27c4; __auc=82242dc5171905553d2e805b881; uid=17585743; __gads=ID=6e60a0028239f012:T=1587266595:S=ALNI_MYh2mllyfrdqpS84Qs2-0DYiLkZjg; _hmt=1; sid=s%3A0eKwcI5tkM9DwHgFDM9Om3wpllPaeufV.7kUGPSIEQM9EiF4eMDiVX%2F5H2Z7GjdeU23e3upZ1cfQ; CNZZDATA1256903590=296048625-1587261896-https%253A%252F%252Fwww.baidu.com%252F%7C1587428763; __asc=c77915c81719a2167d49bbe2cdc; _cnzz_CV1256903590=is-logon%7Clogged-in%7C1587431952859%26urlname%7Cnupb5f3ufz%7C1587431952860',
	'Host': 'huaban.com',
	'Referer': 'https://huaban.com/discovery/beauty/',
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

pic_max = 1000

def is_board_or_discovery(url):
	tag = url.split('/')[-2]
	if tag.isdigit():
		return 'board'
	else:
		return 'discovery'

is_board_or_discovery_tag = is_board_or_discovery(main_page)


def get_first_page_urls(url, tag):
	first_page_response = requests.get(url, headers=my_header)
	first_page_response.encoding='utf-8'
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

	first_page_next_url_id =  get_first_page_urls(url, tag)

	print(first_page_next_url_id)
	
	url = create_next_request_url(first_page_next_url_id)

	print(url)
	while True:
		response = requests.get(url, headers=my_header)
		
		response.encoding= 'utf-8'
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
			next_url_id=pins[-1]['pin_id']
		except IndexError:
			print('指定的pic_max值超过画板图片总数！')
			return
		next_page_url = create_next_request_url(next_url_id)
		
		url = next_page_url
		

def create_next_request_url(id_num):
	return page_url_l + str(id_num) + page_url_r


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

def main():
	path_name = 'github_test'

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

	
