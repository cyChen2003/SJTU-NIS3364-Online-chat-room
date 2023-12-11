from chat import chat
from data.data import *
from login.loginUi import *
class Login(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_success)
        self.user_email = ""
        self.user_password = ""
        self.user_port = 8004
    def showMessage(self, msg,type='info'):
        if type == 'info':
            QMessageBox.information(None, "提示", msg, QMessageBox.Ok)
        elif type == 'warning':
            QMessageBox.warning(None, "警告", msg, QMessageBox.Ok)
    def login_success(self):
        validation_result = self.lineEdit_2.validator().validate(self.lineEdit_2.text(), 0)[0]
        if validation_result != QtGui.QValidator.Acceptable:
            self.showMessage("邮箱格式不正确", "warning")
        else:
            Base_dir = os.path.dirname(os.path.abspath(__file__))
            user_dir = os.path.join(Base_dir, "../user")
            if not os.path.exists(user_dir):
                os.mkdir(user_dir)

            user = self.lineEdit_2.text()
            password = self.lineEdit.text()
            port = self.port.text()
            #转成数字
            port =  int(port)

            md5 = hashlib.md5()
            md5.update(password.encode())
            password = md5.hexdigest()
            self.user_email = user
            self.user_password = password
            self.user_port = port
            result=insert_user(username=self.user_email,password=self.user_password, avatar="./data/avatar.jpg",port=self.user_port)
            filename = os.path.join(user_dir, "user_info.csv")
            if result == False:
                self.showMessage("登录失败,请检查用户名和密码", "warning")
            else:
                self.showMessage("登录成功")

                self.secondWindow = chat.MainWinController(self.user_email)
                self.secondWindow.show()
                self.close()
