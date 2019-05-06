# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AuthorizationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(502, 163)
        MainWindow.setMinimumSize(QtCore.QSize(502, 163))
        MainWindow.setMaximumSize(QtCore.QSize(502, 163))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_Login = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Login.setGeometry(QtCore.QRect(140, 10, 351, 30))
        self.lineEdit_Login.setObjectName("lineEdit_Login")
        self.lineEdit_Password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Password.setGeometry(QtCore.QRect(140, 50, 351, 30))
        self.lineEdit_Password.setObjectName("lineEdit_Password")
        self.Auth_button = QtWidgets.QPushButton(self.centralwidget)
        self.Auth_button.setGeometry(QtCore.QRect(110, 100, 311, 32))
        self.Auth_button.setObjectName("Auth_button")
        self.label_Login = QtWidgets.QLabel(self.centralwidget)
        self.label_Login.setGeometry(QtCore.QRect(20, 15, 111, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Login.sizePolicy().hasHeightForWidth())
        self.label_Login.setSizePolicy(sizePolicy)
        self.label_Login.setTextFormat(QtCore.Qt.RichText)
        self.label_Login.setObjectName("label_Login")
        self.label_Password = QtWidgets.QLabel(self.centralwidget)
        self.label_Password.setGeometry(QtCore.QRect(83, 57, 57, 16))
        self.label_Password.setObjectName("label_Password")
        self.Auth_button.raise_()
        self.lineEdit_Login.raise_()
        self.lineEdit_Password.raise_()
        self.label_Login.raise_()
        self.label_Password.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Авторизация"))
        self.Auth_button.setText(_translate("MainWindow", "Вход в систему"))
        self.label_Login.setText(_translate("MainWindow", "Имя пользователя"))
        self.label_Password.setText(_translate("MainWindow", "Пароль"))


