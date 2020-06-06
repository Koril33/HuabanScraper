# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\GUI\dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.lineEdit_url = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_url.setGeometry(QtCore.QRect(140, 60, 113, 21))
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.lineEdit_path = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_path.setGeometry(QtCore.QRect(140, 110, 113, 21))
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.lineEdit_max = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_max.setGeometry(QtCore.QRect(140, 160, 113, 21))
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 160, 72, 15))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 230, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 230, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Url"))
        self.label_2.setText(_translate("Dialog", "Path"))
        self.label_3.setText(_translate("Dialog", "Max"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
        self.pushButton_2.setText(_translate("Dialog", "PushButton"))
