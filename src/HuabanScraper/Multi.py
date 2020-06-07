from GUI.MultiGUI import Ui_MainWindow
from GUI.Dialog import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import QThread, pyqtSignal, QMessageBox
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import Scraper.HuabanScraper as HuabanScraper

from multiprocessing import Pool
import multiprocessing
import concurrent.futures

class ThreadDownload(QThread):
    # download_proess_signal = pyqtSignal(int)
    # download_message_signal = pyqtSignal(str)
    # download_time_signal = pyqtSignal(int)
    # # download_overtax_signal = pyqtSignal(bool)
    download_finish_signal = pyqtSignal(bool)
    # donwload_count_signal = pyqtSignal(int)

    def __init__(self, urls, pic_maxs, path_names, pic_filters):
        super().__init__()
        self.urls = urls
        self.pic_maxs = pic_maxs
        self.path_names = path_names
        self.pic_filters = pic_filters

        print('__init__')
        # self.overtax = False

    def filter_parse(self, img_filter):
        return tuple(img_filter.split('/'))

    def download_all(self, i, url, pic_max, path_name, pic_filter):
        print('download')
        pic_filter = self.filter_parse(pic_filter)
        print(f'任务{i}开始下载...url:{url}, max:{pic_max}, path:{path_name}, type_filter:{pic_filter}')
        scraper = HuabanScraper.Scraper(url, pic_max, path_name, pic_filter)
        scraper.run_and_download()
        print(f'-----------------任务{i}下载结束---------------------')

    def run(self):
        # p = Pool(4)
        # for i in range(len(self.urls)):
        #     ret = p.apply_async(self.download_all,args=(i, self.urls[i], self.pic_maxs[i], self.path_names[i], self.pic_filters[i]))  # 异步的，一个运行完才执行另一个
        # p.close()
        # p.join()
        for i in range(len(self.urls)):
            self.download_all(i, self.urls[i], self.pic_maxs[i], self.path_names[i], self.pic_filters[i])
        
        self.download_finish_signal.emit(True)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.urls = []
        self.pic_maxs = []
        self.path_names = []
        self.pic_filters = []

    #insert,只是简单插入一个固定数据
    def table_insert(self, url, path_name, pic_max, pic_filter):
        row = self.table.rowCount()
        self.table.insertRow(row)
 
        item_url = QTableWidgetItem(url)
        item_url.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
 
        item_path = QTableWidgetItem(path_name) #我们要求它可以修改，所以使用默认的状态即可
 
        item_max = QTableWidgetItem(pic_max)
        item_max.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择

        item_filter = QTableWidgetItem(pic_filter)

        self.table.setItem(row, 0, item_url)
        self.table.setItem(row, 1, item_path)
        self.table.setItem(row, 2, item_max)
        self.table.setItem(row, 3, item_filter)
        
        #以下可以加入保存数据到数据的操作
 
    #update
    def table_update(self):
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        new_name = row_select[1].text()
        print("id: {}, save_name: {}".format(id,new_name))
        # 以下可以加入保存数据到数据的操作
        '''
        eg. update {table} set name = "new_name" where id = "id"
        '''
 
    #delete
    def ClickDel(self):
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        url = row_select[0].text()
        print("delete url: {}".format(url))

        row = row_select[0].row()
        self.table.removeRow(row)
        del_index = self.urls.index(url)
        self.urls.pop(del_index)
        self.path_names.pop(del_index)
        self.pic_maxs.pop(del_index)
        self.pic_filters.pop(del_index)
        
        # 以下可以加入保存数据到数据的操作
        '''
        eg. delete from {table} where id = "id"
        '''

    # add
    def ClickAdd(self, url, path_name, pic_max, pic_filter):
        self.table_insert(url, path_name, pic_max, pic_filter)

    def create_filter(self, jpg_flag, png_flag, gif_flag):
        if jpg_flag and not png_flag and not gif_flag:
            return 'jpg'
        elif not jpg_flag and png_flag and not gif_flag:
            return 'png'
        elif not jpg_flag and not png_flag and gif_flag:
            return 'gif'
        elif jpg_flag and png_flag and not gif_flag:
            return 'jpg/png'
        elif jpg_flag and not png_flag and gif_flag:
            return 'jpg/gif'
        elif not jpg_flag and png_flag and gif_flag:
            return 'png/gif'
        elif jpg_flag and png_flag and gif_flag:
            return 'jpg/png/gif'

    def ShowDialog(self):
        # 创建子窗口实例
        self.dialog = ChildWindow()
        # 显示子窗口
        self.dialog.show()
        # 实现子窗口中的【确定】按钮功能
        def ButtonOK():
            # 获取下载URL
            self.url = self.dialog.lineEdit_url.text()
            # 获取下载路径
            self.path_name = self.dialog.lineEdit_path.text()
            # 获取下载数量
            self.pic_max = self.dialog.spinBox.text()

            # 获取过滤值
            jpg_flag = self.dialog.checkBox_jpg.isChecked()
            png_flag = self.dialog.checkBox_png.isChecked()
            gif_flag = self.dialog.checkBox_gif.isChecked()
            self.pic_filter = self.create_filter(jpg_flag, png_flag, gif_flag)

            self.urls.append(self.url)
            self.path_names.append(self.path_name)
            self.pic_maxs.append(self.pic_max)
            self.pic_filters.append(self.pic_filter)
            

            self.ClickAdd(self.url, self.path_name, self.pic_max, self.pic_filter)

            self.dialog.close()
        # 关联【确定】按钮
        self.dialog.pushButton.clicked.connect(ButtonOK)
        self.dialog.exec_()

    def DownloadPic(self):
        # self.set_btn_off()
        print('start download...')
        print(f'urls:{self.urls}')
        print(f'pic_maxs:{self.pic_maxs}')
        print(f'path_names:{self.path_names}')
        print(f'pic_filters:{self.pic_filters}')

        self.set_btn_off()
        self.thread_download = ThreadDownload(self.urls, self.pic_maxs, self.path_names, self.pic_filters)
        self.thread_download.download_finish_signal.connect(self.download_finish)
        self.thread_download.start()

    def download_finish(self):
        self.set_btn_on()
    
    def set_btn_off(self):
        '''正在下载时，按钮无法再次点击
        '''

        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setText('正在下载...')

    def set_btn_on(self):
        '''下载完成后，按钮恢复
        '''

        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setText('开始下载')


class ChildWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(ChildWindow, self).__init__()
        self.setupUi(self)

    def find_path(self):
        '''选取本地保存路径
        '''

        download_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                   "选取文件夹",
                                                                   "./")  # 起始路径
        self.lineEdit_path.setText(download_path)

    def clear_and_paste(self):
        self.lineEdit_url.clear()
        self.lineEdit_url.paste()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
