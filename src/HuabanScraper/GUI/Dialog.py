# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\GUI\Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(605, 349)
        self.lineEdit_url = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_url.setGeometry(QtCore.QRect(110, 60, 391, 21))
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.lineEdit_path = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_path.setGeometry(QtCore.QRect(110, 110, 391, 21))
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 160, 72, 15))
        self.label_3.setObjectName("label_3")
        self.button_add = QtWidgets.QPushButton(Dialog)
        self.button_add.setGeometry(QtCore.QRect(240, 270, 121, 51))
        self.button_add.setObjectName("button_add")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 210, 72, 15))
        self.label_4.setObjectName("label_4")
        self.button_select_path = QtWidgets.QPushButton(Dialog)
        self.button_select_path.setGeometry(QtCore.QRect(510, 110, 71, 21))
        self.button_select_path.setObjectName("button_select_path")
        self.checkBox_jpg = QtWidgets.QCheckBox(Dialog)
        self.checkBox_jpg.setGeometry(QtCore.QRect(110, 210, 91, 19))
        self.checkBox_jpg.setObjectName("checkBox_jpg")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(110, 160, 91, 22))
        self.spinBox.setObjectName("spinBox")
        self.checkBox_png = QtWidgets.QCheckBox(Dialog)
        self.checkBox_png.setGeometry(QtCore.QRect(230, 210, 91, 19))
        self.checkBox_png.setObjectName("checkBox_png")
        self.checkBox_gif = QtWidgets.QCheckBox(Dialog)
        self.checkBox_gif.setGeometry(QtCore.QRect(340, 210, 91, 19))
        self.checkBox_gif.setObjectName("checkBox_gif")
        self.button_paste = QtWidgets.QPushButton(Dialog)
        self.button_paste.setGeometry(QtCore.QRect(510, 60, 71, 21))
        self.button_paste.setObjectName("button_paste")

        self.retranslateUi(Dialog)

        self.button_select_path.clicked.connect(Dialog.find_path)
        self.button_paste.clicked.connect(Dialog.clear_and_paste)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Url"))
        self.label_2.setText(_translate("Dialog", "Path"))
        self.label_3.setText(_translate("Dialog", "Max"))
        self.button_add.setText(_translate("Dialog", "添加"))
        self.label_4.setText(_translate("Dialog", "filter"))
        self.button_select_path.setText(_translate("Dialog", "浏览"))
        self.checkBox_jpg.setText(_translate("Dialog", "jpg"))
        self.checkBox_png.setText(_translate("Dialog", "png"))
        self.checkBox_gif.setText(_translate("Dialog", "gif"))
        self.button_paste.setText(_translate("Dialog", "粘贴"))
