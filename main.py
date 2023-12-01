import sys
import login
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import hashlib
from chat_room import *
Base_dir = os.path.dirname(os.path.abspath(__file__))
user_dir = Base_dir + "/user"

# ...



if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    MainWindow = QMainWindow()

    # 创建ui，引用demo1文件中的Ui_MainWindow类
    ui = login.Ui_MainWindow(main_window=MainWindow)
    # 调用Ui_MainWindow类的setupUi，创建初始组件
    ui.setupUi(MainWindow)
    # 创建窗口
    MainWindow.show()
    sys.exit(app.exec_())
