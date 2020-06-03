from GUI.HuabanGUI import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import QThread, pyqtSignal, QMessageBox
import Scraper.HuabanScraper as HuabanScraper
import time
import concurrent.futures
import webbrowser


class ThreadDownload(QThread):
    download_proess_signal = pyqtSignal(int)
    download_message_signal = pyqtSignal(str)
    download_time_signal = pyqtSignal(int)
    # download_overtax_signal = pyqtSignal(bool)
    download_finish_signal = pyqtSignal(bool)
    donwload_count_signal = pyqtSignal(int)

    def __init__(self, url, pic_max, path_name, type_filter):
        super().__init__()
        self.url = url
        self.pic_max = pic_max
        self.path_name = path_name
        self.type_filter = type_filter
        # self.overtax = False

    def download(self, scraper, single_url, index, raw_type):
        '''下载单个图片
        :param scraper: Scraper对象
        :param single_url: 单个图片的url
        :param index: 图片保存代号
        '''

        scraper.download.download_image(single_url, self.path_name, index, raw_type)
        process = int(scraper.download.get_download_count() / int(self.pic_max) * 100)
        msg = f'{single_url} 下载成功！'

        # 发送信号：进度条的值
        self.download_proess_signal.emit(process)
        # 发送信号：面板需要展示的下载信息
        self.download_message_signal.emit(msg)

    def run(self):
        '''下载所有图片
        '''

        scraper = HuabanScraper.Scraper(
            self.url, self.pic_max, self.path_name, self.type_filter)

        # 将所有图片下载路径存入scraper对象的all_urls中
        scraper.run_without_download()
        
        # 发送超过图片总数的信号
        # self.download_overtax_signal.emit(scraper.get_overtax_flag())

        # 计时，开始时间
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for index, single_url in enumerate(scraper.get_all_urls()):
                executor.submit(self.download, 
                                    scraper, 
                                    single_url, 
                                    index, scraper.get_all_urls()[single_url]['img_type'])
        # 计时，结束时间
        end_time = time.time()
        consume_time = int(end_time - start_time)
        # consume_time_msg = f"{'-' * 40}下载耗时：{consume_time} 秒{'-' * 40}"

        # 发送信号：下载耗时
        self.download_time_signal.emit(consume_time)

        # 发送信号，成功下载数量
        self.donwload_count_signal.emit(scraper.download.get_download_count())

        # 发送信号：下载完成
        self.download_finish_signal.emit(True)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        self.bar_value = 0
        # self.overtax_flag = False
        self.consume_time = 0
        self.download_count = 0
        self.pic_max = 0

    def clear_and_paste(self):
        self.lineEdit_url.clear()
        self.lineEdit_url.paste()

    def find_path(self):
        '''选取本地保存路径
        '''

        download_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                   "选取文件夹",
                                                                   "./")  # 起始路径
        self.lineEdit_path.setText(download_path)

    def check_input(self, url, path_name):
        '''检查用户输入
        :param url: 用户填写的下载url
        :param path_name: 用户填写的本地保存路径
        '''

        if url.isspace() or url == '':
            QMessageBox.critical(self, "错误", "请填写下载网址！", QMessageBox.Retry)
            return False
        elif not 'https://huaban.com' in url:
            QMessageBox.critical(
                self, "错误", "请检查网址\n此软件目前仅支持花瓣网！", QMessageBox.Retry)
            return False
        elif path_name.isspace() or path_name == '':
            QMessageBox.critical(self, "错误", "请填写保存路径！", QMessageBox.Retry)
            return False
        else:
            return True

    def start_download(self):
        '''与开始按钮绑定的事件
        '''

        # 获取url
        url = self.lineEdit_url.text()
        # 获取下载路径
        path_name = self.lineEdit_path.text()
        # 获取下载数量
        self.pic_max = self.spinBox.text()
        # 获取下载类型（all，jpg，png，gif）
        all_flag = self.radioButton_all.isChecked()
        jpg_flag = self.checkBox_jpg.isChecked()
        png_flag = self.checkBox_png.isChecked()
        gif_flag = self.checkBox_gif.isChecked()

        if all_flag == True or (jpg_flag and png_flag and gif_flag):
            type_filter = ('jpg', 'png', 'gif')
        elif jpg_flag and not png_flag and not gif_flag:
            type_filter = ('jpg', )
        elif not jpg_flag and png_flag and not gif_flag:
            type_filter = ('png', )
        elif not jpg_flag and not png_flag and gif_flag:
            type_filter = ('gif', )
        elif jpg_flag and png_flag and not gif_flag:
            type_filter = ('jpg', 'png')
        elif jpg_flag and not png_flag and gif_flag:
            type_filter = ('jpg', 'gif')
        elif not jpg_flag and png_flag and gif_flag:
            type_filter = ('png', 'gif')
        

        if self.check_input(url, path_name):
            self.set_btn_off()
            self.thread_download = ThreadDownload(url, self.pic_max, path_name, type_filter)
            self.thread_download.download_proess_signal.connect(
                self.set_progressbar_value)
            self.thread_download.download_message_signal.connect(
                self.download_msg_print)
            self.thread_download.download_time_signal.connect(
                self.set_consume_time)
            # self.thread_download.download_overtax_signal.connect(
            #     self.overtax_handle)
            self.thread_download.download_finish_signal.connect(
                self.download_finish)
            self.thread_download.donwload_count_signal.connect(
                self.set_download_count)

            self.thread_download.start()

    def set_btn_off(self):
        '''正在下载时，按钮无法再次点击
        '''

        self.Button1.setEnabled(False)
        self.Button1.setText('正在下载...')

    def set_btn_on(self):
        '''下载完成后，按钮恢复
        '''

        self.Button1.setEnabled(True)
        self.Button1.setText('开始下载')

    def set_progressbar_value(self, value):
        '''设置进度条
        :param value: download_proess_signal，进度条的值
        '''
        self.bar_value = value
        self.progressBar.setValue(value)

    def set_consume_time(self, consume_time):
        '''记录下载消耗时间
        :param consume_time: download_time_signal，消耗的时间
        '''
        self.consume_time = consume_time

    def set_download_count(self, donwload_count):
        self.download_count = donwload_count

    # def overtax_handle(self, flag):
    #     '''处理用户指定下载数量超过画板图片总和
    #     :param flag: download_overtax_signal，用户指定数量超过图片总数的信号
    #     '''
    #     self.overtax_flag = flag

    def download_finish(self, flag):
        '''下载成功后的一些提示，还原成员变量的值
        :param flag: download_finish_signal，下载完成的信号
        '''

        if flag:
            QMessageBox.information(self, '提示', '下载成功！', QMessageBox.Ok)
            self.download_msg_print(
                f'[INFO] 消耗时间: {self.consume_time} 秒')
            self.download_msg_print(
                f'[INFO] 成功下载数量：{self.download_count} 张')
            if self.bar_value != 100:
                self.download_msg_print(
                    f'[WARNING] 指定下载数量({self.pic_max}) '
                    f'超过 画板图片总和({self.download_count})！')

            # return
            self.set_btn_on()
            self.progressBar.setValue(0)
            # self.overtax_flag = False

    def download_msg_print(self, msg):
        '''将下载信息显示到面板上
        :param msg: 下载信息
        '''

        self.textBrowser.append(msg)
        self.cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursot.End)

    def author_msg_print(self):
        '''作者信息
        '''

        QMessageBox.about(self, '关于', '版本号：v1.2.0\n'
                                        '--------------------------------------------------------------\n'
                                        '作者：Koril\n'
                                        '--------------------------------------------------------------\n'
                                        '邮箱：dingjinghui33@163.com\n'
                                        '--------------------------------------------------------------\n'
                                        '项目地址：https://github.com/Koril33/HuabanScraper\n'
                                        '--------------------------------------------------------------\n')
                                        

    def open_huaban_web(self):
        '''打开外部网站
        '''

        try:
            webbrowser.get('chrome').open_new_tab('https://huaban.com')
        except Exception as e:
            webbrowser.open_new_tab('https://huaban.com')


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # 创建启动界面
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('res\splash.png'))
    splash.show()

    # 可以显示启动信息
    # splash.showMessage('正在加载……')

    window = MyWindow()

    # 加载qss文件
    styleFile = './style/beautify.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    window.setStyleSheet(qssStyle)

    window.show()

    # 关闭启动画面
    splash.close()

    sys.exit(app.exec_())
