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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 350, 100, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 350, 100, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(710, 350, 100, 50))
        self.pushButton_3.setObjectName("pushButton_3")


        self.table = QTableWidget(self)
        self.table.move(20, 20)
        self.table.setColumnCount(4)

        # 调整列宽
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.table.setFixedHeight(300)
        self.table.setFixedWidth(960)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)#设置表格的选取方式是行选取
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)#设置选取方式为单个选取
        self.table.setHorizontalHeaderLabels(["URL地址", "下载文件夹", "图片数量", "图片类型过滤"]) #设置行表头
        self.table.verticalHeader().setVisible(False)#隐藏列表头
        
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

        self.pushButton.clicked.connect(MainWindow.ShowDialog)
        self.pushButton_2.clicked.connect(MainWindow.ClickDel)
        self.pushButton_3.clicked.connect(MainWindow.DownloadPic)


        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "新建"))
        self.pushButton_2.setText(_translate("MainWindow", "删除"))
        self.pushButton_3.setText(_translate("MainWindow", "开始下载"))
