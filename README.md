# HuabanScraper
* 花瓣网爬虫，自动下载图片
* 多线程下载
* 可以指定下载图片的数量
* 两种下载方式，一种是使用selenium，一种是使用requests

---

## selenium + BeautifulSoup的方式

方法直观，但速度较慢

---

## requests+json的方式

直接解析json中图片的key值，获取图片下载地址，速度很快。

* 本地环境：Windows，python3.7
* 额外需要下载的库：requests

如果没有安装requests，使用命令：`pip install requests`。

### 使用方法

格式：

```
python huaban_by_requests.py --url [URL] --max [MAX_NUM] --path [FOLDER_NAME]
```

需要有三个参数

1. `--url`，需要下载的url（必选参数），例如：

   > https://huaban.com/discovery/beauty/
   >
   > https://huaban.com/boards/3114850/
   >
   > https://huaban.com/boards/3114850/?k99otknb&max=2857420870&limit=20&wfl=1

2. `--max`，下载图片最大数量（不指定此参数的话，默认下载10张）如果设置的数量超过画板内图片的总数，则将此画板所有图片下载下来。

3. `--path`，文件夹名字（不指定此参数的话，默认名字为‘huaban_pictures’），用来新建一个文件夹，保存下载的图片。

```
python huaban_by_requests.py --url 'https://huaban.com/discovery/beauty/' --max '30' --path '测试'
```

上面这行命令，就是从指定的网页上下载前30张图片，并保存到名为“测试”的文件夹下。

---

## 注意

最好将url参数用引号包裹起来，不然如果你的URL是这种：

>https://huaban.com/boards/3114850/?k99otknb&max=2857420870&limit=20&wfl=1

cmd就会报错。改成如下格式即可：

```
python huaban_by_requests.py --url 'https://huaban.com/boards/3114850/?k99otknb&max=2857420870&limit=20&wfl=1'
```

---

### exe方式

源文件已经打包成了exe格式，位于dist目录下。格式和上面一样，打开cmd，进入存放exe文件的目录下，输入命令：

```
huaban_command.exe --url https://huaban.com/explore/piqiaqiubizhi/ --max 50 --path 皮卡丘壁纸
```

