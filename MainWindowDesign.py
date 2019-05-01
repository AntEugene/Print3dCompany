# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './MainWindowDesign.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 555)
        Dialog.setMinimumSize(QtCore.QSize(800, 555))
        Dialog.setMaximumSize(QtCore.QSize(800, 555))
        self.Button_Add = QtWidgets.QPushButton(Dialog)
        self.Button_Add.setGeometry(QtCore.QRect(580, 510, 85, 32))
        self.Button_Add.setObjectName("Button_Add")
        self.Button_Show = QtWidgets.QPushButton(Dialog)
        self.Button_Show.setGeometry(QtCore.QRect(480, 510, 85, 32))
        self.Button_Show.setObjectName("Button_Show")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 801, 491))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.lineEdit_TableName = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_TableName.setGeometry(QtCore.QRect(150, 510, 311, 30))
        self.lineEdit_TableName.setObjectName("lineEdit_TableName")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 510, 121, 31))
        self.label.setObjectName("label")
        self.Button_Save = QtWidgets.QPushButton(Dialog)
        self.Button_Save.setGeometry(QtCore.QRect(680, 510, 111, 32))
        self.Button_Save.setObjectName("Button_Save")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Button_Add.setText(_translate("Dialog", "Добавить"))
        self.Button_Show.setText(_translate("Dialog", "Показать"))
        self.label.setText(_translate("Dialog", "Название таблицы:"))
        self.Button_Save.setText(_translate("Dialog", "Сохранить в БД"))


