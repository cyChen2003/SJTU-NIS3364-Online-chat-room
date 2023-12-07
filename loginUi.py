# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget, QLabel, QFormLayout, QSizePolicy, QMessageBox
import os
import hashlib
import chat_room
class Ui_MainWindow(object):
    # def __init__(self,main_window):
    #     self.main_window = main_window
    #     self.setupUi(main_window)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(271, 222, 311, 181))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLaout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLaout_3.setObjectName("horizontalLayout")

        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("请输入邮箱")
        email_validator = QRegExpValidator(QRegExp(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"))
        self.lineEdit_2.setValidator(email_validator)
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setPlaceholderText("请输入密码")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.port_label = QtWidgets.QLabel(self.layoutWidget)
        self.port_label.setObjectName("port_label")
        self.horizontalLaout_3.addWidget(self.port_label)
        self.port = QtWidgets.QLineEdit()
        self.port.setPlaceholderText("请输入端口号")
        self.horizontalLaout_3.addWidget(self.port)
        self.verticalLayout.addLayout(self.horizontalLaout_3)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 33))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "欢迎使用交我聊小程序"))
        self.label.setText(_translate("MainWindow", "邮箱"))
        self.label_2.setText(_translate("MainWindow", "密码"))
        self.port_label.setText(_translate("MainWindow", "端口号"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
    #     self.pushButton.clicked.connect(self.login_success)
    # def showMessage(self, msg,type='info'):
    #     if type == 'info':
    #         QMessageBox.information(None, "提示", msg, QMessageBox.Ok)
    #     elif type == 'warning':
    #         QMessageBox.warning(None, "警告", msg, QMessageBox.Ok)
    # def login_success(self):
    #     validation_result = self.lineEdit_2.validator().validate(self.lineEdit_2.text(), 0)[0]
    #     if validation_result != QtGui.QValidator.Acceptable:
    #         self.showMessage("邮箱格式不正确", "warning")
    #     else:
    #         Base_dir = os.path.dirname(os.path.abspath(__file__))
    #         self.showMessage("登录成功")
    #         user_dir = os.path.join(Base_dir, "user")
    #         if not os.path.exists(user_dir):
    #             os.mkdir(user_dir)
    #
    #         user = self.lineEdit_2.text()
    #         password = self.lineEdit.text()
    #
    #         md5 = hashlib.md5()
    #         md5.update(password.encode())
    #         password = md5.hexdigest()
    #
    #         filename = os.path.join(user_dir, "user_info.csv")
    #         with open(filename, "a", encoding="utf-8") as f:
    #             f.write(user + "," + password + "\n")
    #         self.secondWindow = chat_room.ChatRoom()
    #         self.secondWindow.show()
    #         self.main_window.close()
