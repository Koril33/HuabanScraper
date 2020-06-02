# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\huabanGUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(842, 519)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Button1 = QtWidgets.QPushButton(self.centralwidget)
        self.Button1.setGeometry(QtCore.QRect(640, 110, 151, 51))
        self.Button1.setObjectName("Button1")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(20, 40, 91, 41))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 140, 72, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 72, 15))
        self.label_3.setObjectName("label_3")
        self.lineEdit_url = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_url.setGeometry(QtCore.QRect(110, 50, 381, 21))
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.lineEdit_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_path.setGeometry(QtCore.QRect(110, 100, 381, 21))
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(110, 150, 101, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(9999999)
        self.spinBox.setObjectName("spinBox")
        self.Button2 = QtWidgets.QPushButton(self.centralwidget)
        self.Button2.setGeometry(QtCore.QRect(510, 100, 93, 21))
        self.Button2.setObjectName("Button2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(240, 150, 361, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 270, 801, 191))
        self.textBrowser.setObjectName("textBrowser")
        self.Button3 = QtWidgets.QPushButton(self.centralwidget)
        self.Button3.setGeometry(QtCore.QRect(510, 50, 93, 21))
        self.Button3.setObjectName("Button3")
        self.Button4 = QtWidgets.QPushButton(self.centralwidget)
        self.Button4.setGeometry(QtCore.QRect(640, 50, 151, 51))
        self.Button4.setObjectName("Button4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 200, 72, 41))
        self.label_4.setObjectName("label_4")
        self.radioButton_all = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_all.setGeometry(QtCore.QRect(110, 210, 115, 19))
        self.radioButton_all.setChecked(False)
        self.radioButton_all.setObjectName("radioButton_all")
        self.checkBox_jpg = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_jpg.setGeometry(QtCore.QRect(220, 210, 91, 19))
        self.checkBox_jpg.setObjectName("checkBox_jpg")
        self.checkBox_png = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_png.setGeometry(QtCore.QRect(330, 210, 91, 19))
        self.checkBox_png.setObjectName("checkBox_png")
        self.checkBox_gif = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_gif.setGeometry(QtCore.QRect(440, 210, 91, 19))
        self.checkBox_gif.setObjectName("checkBox_gif")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 842, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionauthor = QtWidgets.QAction(MainWindow)
        self.actionauthor.setObjectName("actionauthor")
        self.menu.addAction(self.actionauthor)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        
        self.setWindowOpacity(0.9) # 设置窗口透明度
        
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明

        # 添加按钮事件绑定
        self.Button1.clicked.connect(MainWindow.start_download)
        self.Button2.clicked.connect(MainWindow.find_path)

        # 添加菜单栏作者信息提示
        self.actionauthor.triggered.connect(MainWindow.author_msg_print)

        # 粘贴剪切板
        self.Button3.clicked.connect(self.clear_and_paste)

        # 打开花瓣网
        self.Button4.clicked.connect(self.open_huaban_web)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "花瓣图片下载器"))
        self.Button1.setText(_translate("MainWindow", "开始下载"))
        self.label_1.setText(_translate("MainWindow", "图片网址"))
        self.label_2.setText(_translate("MainWindow", "下载数量"))
        self.label_3.setText(_translate("MainWindow", "下载路径"))
        self.Button2.setText(_translate("MainWindow", "浏览"))
        self.Button3.setText(_translate("MainWindow", "粘贴链接"))
        self.Button4.setText(_translate("MainWindow", "花瓣官网"))
        self.label_4.setText(_translate("MainWindow", "下载类型"))
        self.radioButton_all.setText(_translate("MainWindow", "All"))
        self.checkBox_jpg.setText(_translate("MainWindow", "JPG"))
        self.checkBox_png.setText(_translate("MainWindow", "PNG"))
        self.checkBox_gif.setText(_translate("MainWindow", "GIF"))
        self.menu.setTitle(_translate("MainWindow", "About"))
        self.actionauthor.setText(_translate("MainWindow", "author"))
