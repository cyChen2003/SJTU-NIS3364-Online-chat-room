import sys
import login

from PyQt5.QtWidgets import QApplication,QMainWindow
import os
import hashlib
Base_dir = os.path.dirname(os.path.abspath(__file__))
user_dir = Base_dir + "/user"

# ...

def click_success():
    print("登录成功")
    #获取用户输入的用户名和密码
    user = ui.lineEdit_2.text()
    password = ui.lineEdit.text()
    print(user, password)
    print(type(user), type(password))
    user_dir = Base_dir + "/user"
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    # 使用md5加密password
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    # Corrected the filename creation
    filename = os.path.join(user_dir, "user_info.csv")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(user + "," + password + "\n")

if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    mainWindow = QMainWindow()

    # 创建ui，引用demo1文件中的Ui_MainWindow类
    ui = login.Ui_MainWindow()
    # 调用Ui_MainWindow类的setupUi，创建初始组件
    ui.setupUi(mainWindow)
    # 创建窗口
    mainWindow.show()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    ui.pushButton.clicked.connect(click_success)

    sys.exit(app.exec_())
