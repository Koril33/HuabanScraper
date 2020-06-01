import os
def make_download_dir(path_name):
    '''创建下载图片的文件夹
    :param path: 文件夹名字
    '''

    if not os.path.exists(path_name):
        os.mkdir(path_name)
    else:
        print(f'{path_name} exists!')
