import sys
import loginUi
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import hashlib
from login import *
from chat_room import *
from chat import *
Base_dir = os.path.dirname(os.path.abspath(__file__))
user_dir = Base_dir + "/user"

# ...



if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 实例化窗口
    window = Login()
    window.show()
    sys.exit(app.exec_())

