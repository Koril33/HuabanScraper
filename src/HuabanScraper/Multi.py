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
from Utils.ReadQSS import ReadQSS


class ThreadDownload(QThread):
    # 所有任务下载完成的信号
    download_finish_signal = pyqtSignal(bool)
    # 单个任务完成的信号，用来下载记录历史
    download_single_task_finish_signal = pyqtSignal(int)

    def __init__(self, urls, pic_maxs, path_names, pic_filters):
        super().__init__()
        self.urls = urls
        self.pic_maxs = pic_maxs
        self.path_names = path_names
        self.pic_filters = pic_filters

    def filter_parse(self, img_filter):
        '''解析图片格式的值
        :img_filter: 用户希望下载的格式
        :return: 格式组成的元组，如：输入'jpg/png/gif'，返回('jpg', 'png', 'gif')
        '''

        return tuple(img_filter.split('/'))

    def download_single_task(self, i, url, pic_max, path_name, pic_filter):
        '''下载单个任务
        :param i: 任务的序号
        :param url: 需要下载的url
        :param pic_max: 最大下载图片数量
        :param path_name: 保存的路径
        :param pic_filter: 用户希望下载的格式
        :return:
        '''

        pic_filter = self.filter_parse(pic_filter)
        print(
            f'任务{i}开始下载...url:{url}, max:{pic_max}, path:{path_name}, type_filter:{pic_filter}')
        scraper = HuabanScraper.Scraper(url, pic_max, path_name, pic_filter)
        scraper.run_and_download()
        print(f'-----------------任务{i}下载结束---------------------')

    def run(self):
        # p = Pool(4)
        # for i in range(len(self.urls)):
        #     ret = p.apply_async(self.download_single_task,args=(i, self.urls[i], self.pic_maxs[i], self.path_names[i], self.pic_filters[i]))  # 异步的，一个运行完才执行另一个
        # p.close()
        # p.join()
        for i in range(len(self.urls)):
            self.download_single_task(
                i, self.urls[i], self.pic_maxs[i], self.path_names[i], self.pic_filters[i])
            # 每完成一个任务，发射一次信号
            self.download_single_task_finish_signal.emit(i)
        # 所有下载任务完成，发射完成信号
        self.download_finish_signal.emit(True)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.urls = []
        self.pic_maxs = []
        self.path_names = []
        self.pic_filters = []

        self.history = []

    def table_insert(self, url, path_name, pic_max, pic_filter):
        '''表格插入新建的任务信息
        :param url: 需要下载的url
        :param pic_max: 最大下载图片数量
        :param path_name: 保存的路径
        :param pic_filter: 用户希望下载的格式
        :return:
        '''

        # 插入到最后一行
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_url = QTableWidgetItem(url)
        # 设置物件的状态为只可被选择（未设置可编辑）
        item_url.setFlags(Qt.ItemIsSelectable |
                          Qt.ItemIsEnabled)
        # 要求它可以修改，所以使用默认的状态即可
        item_path = QTableWidgetItem(path_name)

        item_max = QTableWidgetItem(pic_max)
        # 设置物件的状态为只可被选择
        item_max.setFlags(Qt.ItemIsSelectable |
                          Qt.ItemIsEnabled)

        item_filter = QTableWidgetItem(pic_filter)

        self.table.setItem(row, 0, item_url)
        self.table.setItem(row, 1, item_path)
        self.table.setItem(row, 2, item_max)
        self.table.setItem(row, 3, item_filter)

    def table_update(self):
        '''当表格任务更新时，获取更新的数据
        '''

        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        new_name = row_select[1].text()
        print("id: {}, save_name: {}".format(id, new_name))

    def click_delete(self):
        '''用户单击主页面的删除键
        '''

        # 获取删除的行号
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        url = row_select[0].text()
        print("delete url: {}".format(url))

        row = row_select[0].row()
        self.table.removeRow(row)

        # 通过url定位删除的索引
        del_index = self.urls.index(url)
        # 根据删除索引，删掉对应的path_name,pic_max，pic_filter
        self.urls.pop(del_index)
        self.path_names.pop(del_index)
        self.pic_maxs.pop(del_index)
        self.pic_filters.pop(del_index)

    # add
    def click_add(self, url, path_name, pic_max, pic_filter):
        '''用户在‘新建任务’的对话栏中，输入完信息后
           将信息保存，并插入到表格中
        '''

        self.table_insert(url, path_name, pic_max, pic_filter)

    def create_filter(self, jpg_flag, png_flag, gif_flag):
        '''根据check_box的勾选情况进行分类
        :param jpg_flag: check_box_jpg的值
        :param png_flag: check_box_png的值
        :param gif_flag: check_box_gif的值
        '''

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

    def show_new_task_dialog(self):
        '''用户单击主界面上的'新建'按钮后，生成对话框
           用来输入任务的各项信息
        '''

        # 创建子窗口实例
        self.dialog = ChildWindow()

        # 通过qss美化窗口
        styleFile = './style/multi.qss'
        qssStyle = ReadQSS.read_qss(styleFile)
        self.dialog.setStyleSheet(qssStyle)

        # 显示子窗口
        self.dialog.show()

        # 当用户单击新建任务对话框中的'添加'按钮后，保存各项信息
        def click_new():
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

            self.click_add(self.url, self.path_name,
                           self.pic_max, self.pic_filter)

            self.dialog.close()
        # 关联'添加'按钮
        self.dialog.button_add.clicked.connect(click_new)
        self.dialog.exec_()

    def download_pic(self):
        '''当用户单击主界面的'下载'按钮后
           开始下载图片
        '''

        print('start download...')
        print(f'urls:{self.urls}')
        print(f'pic_maxs:{self.pic_maxs}')
        print(f'path_names:{self.path_names}')
        print(f'pic_filters:{self.pic_filters}')

        # 将下载按钮设置为不可点击状态
        self.set_btn_off()
        # 开始下载子线程
        self.thread_download = ThreadDownload(
            self.urls, self.pic_maxs, self.path_names, self.pic_filters)
        # 接收完成信号
        self.thread_download.download_finish_signal.connect(
            self.download_finish)
        # 接收单个任务完成信号
        self.thread_download.download_single_task_finish_signal.connect(
            self.download_single_task_finish)
        self.thread_download.start()

    def download_single_task_finish(self, row):
        '''保存下载记录
        '''

        self.history.append(self.table.item(0, 0).text())
        self.table.removeRow(0)
        print(self.history)

    def download_finish(self):
        '''和所有任务下载完成的信号绑定
        '''

        # 全部下载完成后，清空任务队列
        self.urls = []
        self.path_names = []
        self.pic_maxs = []
        self.pic_filters = []

        # 弹出提示信息
        QMessageBox.information(self, '提示', '所有任务下载完成！', QMessageBox.Ok)

        # 将'下载'按钮设置为可以使用的状态
        self.set_btn_on()

    def set_btn_off(self):
        '''正在下载时，按钮无法再次点击
        '''

        self.button_download.setEnabled(False)
        self.button_download.setText('正在下载...')

    def set_btn_on(self):
        '''下载完成后，按钮恢复
        '''

        self.button_download.setEnabled(True)
        self.button_download.setText('开始下载')


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
        '''清空url输入框并粘贴
        '''

        self.lineEdit_url.clear()
        self.lineEdit_url.paste()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()

    # 通过qss美化窗口
    styleFile = './style/multi.qss'
    qssStyle = ReadQSS.read_qss(styleFile)
    window.setStyleSheet(qssStyle)

    window.show()
    sys.exit(app.exec_())
