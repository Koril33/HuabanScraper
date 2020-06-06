from GUI.MultiGUI import Ui_MainWindow
from GUI.Dialog import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import QThread, pyqtSignal, QMessageBox
import time
from PyQt5.QtWidgets import *



class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    def LineEditAdd(self, txt):
        line = QLineEdit(self)
        line.setText(txt)
        return line

        #删除槽
    def ClickDel(self):
        print(self.listWidget.count())

        #删除item
        self.listWidget.takeItem(0)

    # 新增槽
    def ClickAdd(self, txt):
        # 新增line
        addline = self.LineEditAdd(txt)
        
        #将新增按钮添加到列表中
        additem = QListWidgetItem()
        self.listWidget.addItem(additem)
        self.listWidget.setItemWidget(additem,addline)


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
            self.pic_max = self.dialog.lineEdit_max.text()

            self.ClickAdd(self.url)
            self.ClickAdd(self.path_name)
            self.ClickAdd(self.pic_max)
            self.dialog.close()
        # 关联【确定】按钮
        self.dialog.pushButton.clicked.connect(ButtonOK)
        self.dialog.exec_()

class ChildWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(ChildWindow, self).__init__()
        self.setupUi(self)




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
