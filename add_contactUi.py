import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from data.data import *
class Add_contact_ui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(200,100)
        self.setWindowTitle('添加联系人')
        self.setWindowIcon(QIcon('./data/icon.png'))
        self.h1_layout = QHBoxLayout()
        self.contact_name = QLabel('联系人端口号:')
        self.contact_name_edit = QLineEdit()
        #正则限制，只能输入数字，末尾是\n
        reg = QRegExp("[0-9]+$")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.contact_name_edit.setValidator(pValidator)
        self.h1_layout.addWidget(self.contact_name)
        self.h1_layout.addWidget(self.contact_name_edit)
        self.add_button = QPushButton('添加')

        # self.add_button.clicked.connect(self.add_contact)
        self.h1_layout.addWidget(self.add_button)
        self.setLayout(self.h1_layout)
        self.show()



