# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\GUI\MultiGUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_new_task = QtWidgets.QPushButton(self.centralwidget)
        self.button_new_task.setGeometry(QtCore.QRect(110, 350, 100, 50))
        self.button_new_task.setObjectName("button_new_task")
        self.button_delete = QtWidgets.QPushButton(self.centralwidget)
        self.button_delete.setGeometry(QtCore.QRect(410, 350, 100, 50))
        self.button_delete.setObjectName("button_delete")
        self.button_download = QtWidgets.QPushButton(self.centralwidget)
        self.button_download.setGeometry(QtCore.QRect(710, 350, 100, 50))
        self.button_download.setObjectName("button_download")

        self.table = QTableWidget(self)
        self.table.move(20, 20)
        self.table.setColumnCount(4)

        # 调整列宽
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents)

        self.table.setFixedHeight(300)
        self.table.setFixedWidth(960)

        # 设置表格的选取方式是行选取
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows)

        # 设置选取方式为单个选取
        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection)

        # 设置行表头
        self.table.setHorizontalHeaderLabels(
            ["URL地址", "下载文件夹", "图片数量", "图片类型过滤"])

        # 隐藏列表头
        self.table.verticalHeader().setVisible(False)

        # 绑定更新事件
        self.table.itemChanged.connect(self.table_update)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 485, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        # 单击'新建'按钮弹出新建任务对话框
        self.button_new_task.clicked.connect(MainWindow.show_new_task_dialog)
        # 单击'删除'按钮删除选中任务条目
        self.button_delete.clicked.connect(MainWindow.click_delete)
        # 单击'下载'按钮开始下载
        self.button_download.clicked.connect(MainWindow.download_pic)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_new_task.setText(_translate("MainWindow", "新建"))
        self.button_delete.setText(_translate("MainWindow", "删除"))
        self.button_download.setText(_translate("MainWindow", "开始下载"))
