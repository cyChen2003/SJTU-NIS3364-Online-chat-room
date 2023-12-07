import socket  # 导入socket模块
import datetime
import json
from add_contactUi import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from data import data
from chatUi import *
import pymysql
import socket
import threading


# from PyQt5.QtWebEngineWidgets import QWebEngineView
class MainWinController(QMainWindow, Ui_Dialog):
    def __init__(self,username,parent=None):

        super(MainWinController, self).__init__(parent)
        self.username=username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.user_port = data.search_port(self.username)
        address = ('localhost', self.user_port)
        self.socket.bind(address)
        self.setWindowTitle('WeChat')
        self.setWindowIcon(QIcon('./data/icon.png'))
        self.setupUi(self)
        self.initui()
        self.showChat()
        self.btn_sendMsg.clicked.connect(self.sendMsg)
        self.my_avatar_dir = data.get_avatar(self.username)

        self.ta_port = None
        self.ta_username = 0  # todo 测试，待改

        self.showAvatar(self.my_avatar_dir, self.myavatar)
        self.Thread = chatMsg(self.username, self.ta_username, self.socket)#id=0测试
        self.Thread.isSend_signal.connect(self.showMsg)
        self.Thread.recvSignal.connect(self.showMsg)
        self.Thread.sendSignal.connect(self.showMsg)
        self.Thread.start()

        self.recvThread = recvThread(username, self.socket)  # 创建新的线程用于接收消息
        self.recvThread.recv_userSignal.connect(
            self.showMsg)
        self.recvThread.start()
        self.textEdit.setFocus()
        self.now_btn = self.btn_chat
        self.last_btn = None
        self.chat_flag = True
        self.showChat()



        self.last_msg_time = datetime.datetime(2023, 12, 19, 15, 4)  # 上次信息的时间
        self.last_talkerId = None
        self.now_talkerId = None

    def showAvatar(self, path, contact):
        pixmap = QPixmap(path).scaled(120, 120)  # 按指定路径找到图片
        contact.setPixmap(pixmap)
    def sendMsg(self):
        msg = self.textEdit.toPlainText()
        message = self.Thread.send_msg(msg, type='G')
        if message == -1:
            print(msg, '发送失败')
            QMessageBox.critical(self, "错误", "对方不在线")
            # self.showMsg(message)
        else:
            print(msg, '发送成功')

        self.textEdit.clear()

    def initui(self):
        self.frame_coninfo = QtWidgets.QFrame(self.frame_2)
        self.frame_coninfo.setGeometry(QtCore.QRect(321, 0, 800, 720))
        self.frame_coninfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_coninfo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_coninfo.setObjectName("frame_coninfo")
        self.frame_coninfo.setVisible(False)
        self.textEdit = myTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(9, 580, 821, 141))
        font = QtGui.QFont("宋体")
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setTabStopWidth(80)
        self.textEdit.setCursorWidth(1)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.sendSignal.connect(self.sendMsg)
        self.btn_sendMsg = QtWidgets.QPushButton(self.frame)
        self.btn_sendMsg.setGeometry(QtCore.QRect(680, 670, 121, 51))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.btn_sendMsg.setFont(font)
        self.btn_sendMsg.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btn_sendMsg.setMouseTracking(False)
        self.btn_sendMsg.setAutoFillBackground(False)
        self.btn_sendMsg.setStyleSheet("QPushButton {background-color: #f0f0f0;\n"
                                       "padding: 10px;\n"
                                       "color:rgb(5,180,104);}\n"
                                       "QPushButton:hover{background-color: rgb(198,198,198)}\n"
                                       )

        self.btn_addC.clicked.connect(self.show_add_contact)
        self.btn_sendMsg.setIconSize(QtCore.QSize(40, 40))
        self.btn_sendMsg.setCheckable(False)
        self.btn_sendMsg.setAutoDefault(True)
        self.btn_sendMsg.setObjectName("btn_sendMsg")
        _translate = QtCore.QCoreApplication.translate
        self.btn_sendMsg.setText(_translate("Dialog", "发送"))
        self.btn_sendMsg.setToolTip('按Enter键发送，按Ctrl+Enter键换行')
        #点击关闭按钮修改online为0
    def closeEvent(self, event):
        data.offline(self.username)
    def show_add_contact(self):
        self.add_contact = Add_contact_ui()
        self.add_contact.show()
        self.add_contact.add_button.clicked.connect(self.set_contact)
    def set_contact(self):
        self.ta_port = int(self.add_contact.contact_name_edit.text())
        if self.ta_port != self.user_port:
            self.ta_username,online = data.use_port_get_username(self.ta_port,type="offline")
            self.Thread.update(self.username, self.ta_username, self.socket)
            if online == 0:
                QMessageBox.information(self, "提示", "添加失败,用户不在线", QMessageBox.Ok)
            else:
                self.label.setText(str(self.ta_username+' '+'在线'))
                QMessageBox.information(self, "提示", "添加成功", QMessageBox.Ok)
                self.add_contact.close()
            if self.ta_username==0:
                QMessageBox.information(self, "提示", "添加失败,用户不存在", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "提示", f"不能添加自己端口，当前端口号{self.user_port}", QMessageBox.Ok)
        #关闭窗口

    def showMsg(self, message):
        """
        显示聊天消息
        :param message:
        :return:
        """
        ta_username = message[5]
        self.ta_username = ta_username
        self.ta_port = data.search_port(self.ta_username)
        self.Thread.update(self.username, self.ta_username, self.socket)
        if (self.ta_username is None
                or ta_username == self.username
        ):
            return
        isSend = message[2]
        content = message[4]
        msg_time = message[3]
        self.check_time(msg_time)
        if isSend == 1:
            # 自己发的信息在右边显示
            self.right(content)
        else:
            # 收到的信息在左边显示
            self.left(content,data.get_avatar(ta_username))
        self.message.moveCursor(self.message.textCursor().End)

    def right(self, content):
        html = '''
            <div>
            <table align="right" style="vertical-align: middle;">
        	<tbody>
        		<tr>
        			<td>%s :</td>
        			<td style="border: 1px #000000 solid"><img align="right" src="%s" width="45" height="45"/></td>
        			<td width="15"></td>
        		</tr>
        	</tbody>
        </table>
        </div>
        ''' % (content, self.my_avatar_dir)
        self.message.insertHtml(html)

    def left(self, content,ta_avatar):
        html = '''
        <div>
                   <table align="left" style="vertical-align: middle;">
                	<tbody>
                		<tr>
                		    <td width="15"></td>
                			<td style="border: 1px #000000 solid"><img align="right" src="%s" width="45" height="45"/></td>
                			<td>: %s</td>
                		</tr>
                	</tbody>
                </table>
                </div>
                ''' % (ta_avatar, content)
        self.message.insertHtml(html)
    def check_time(self, msg_time):
        """
        判断两次聊天时间是否大于五分钟
        超过五分钟就显示时间
        :param msg_time:
        :return:
        """
        dt = msg_time - self.last_msg_time
        # print(msg_time)
        if dt.seconds >= 300:
            html = '''
            <table align="center" style="vertical-align: middle;">
        	<tbody>
        		<tr>
        			<td>%s</td>
        		</tr> 
        	</tbody>
        </table>''' % (msg_time.strftime("%Y-%m-%d %H:%M"))
            # print(html)
            self.last_msg_time = msg_time
            self.message.insertHtml(html)
    def showChat(self):
        """
        显示聊天界面
        :return:
        """
        self.frame_2.setVisible(True)
        # self.GroupView.setVisible(False)
        # self.MyInfoUi.setVisible(False)
        self.frame_coninfo.setVisible(False)
        self.frame.setVisible(True)
        self.now_btn = self.btn_chat
        self.now_btn.setStyleSheet(
            "QPushButton {background-color: rgb(198,198,198);}")
        # if self.last_btn and self.last_btn != self.now_btn:
        #     self.last_btn.setStyleSheet("QPushButton {background-color: rgb(240,240,240);}"
        #                                 "QPushButton:hover{background-color: rgb(209,209,209);}\n")
        # self.last_btn = self.btn_chat
        # self.chat_flag = True
        # contacts = data.get_contacts(self.Me.username)
        # print(contacts)
        # self.contacts_num = len(contacts)
        # max_hight = max(len(contacts) * 80, 680)
        # self.scrollAreaWidgetContents.setGeometry(
        #     QtCore.QRect(0, 0, 300, max_hight))
        # for i in range(len(contacts)):
        #     contact = contacts[i]
        #     # print(contact)
        #     talkerId = contact[0]
        #     conRemark = contact[1]
        #     if talkerId in self.contacts.keys():
        #         print(conRemark)
        #         self.contacts[talkerId].remark1.setText(conRemark)
        #         continue
        #     print('联系人：', i, contact)
            # pushButton_2 = Contact(self.scrollAreaWidgetContents, i, contact)
            # pushButton_2.setGeometry(QtCore.QRect(0, 80 * i, 300, 80))
            # pushButton_2.setLayoutDirection(QtCore.Qt.LeftToRight)
            # pushButton_2.clicked.connect(pushButton_2.show_msg)
            # pushButton_2.usernameSingal.connect(self.Chat)
            # self.contacts[talkerId] = pushButton_2

class myTextEdit(QtWidgets.QTextEdit):  # 继承 原本组件
    sendSignal = pyqtSignal(str)

    def __init__(self, parent):
        QtWidgets.QTextEdit.__init__(self, parent)
        self.parent = parent
        _translate = QtCore.QCoreApplication.translate
        self.setHtml(_translate("Dialog",
                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                "p, li { white-space: pre-wrap; }\n"
                                "</style></head><body style=\" font-family:\'SimSun\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

    def keyPressEvent(self, event):
        QtWidgets.QTextEdit.keyPressEvent(self, event)
        if event.key() == Qt.Key_Return:  # 如果是Enter 按钮
            modifiers = event.modifiers()
            if modifiers == Qt.ControlModifier:
                print('success press ctrl+enter key', self.toPlainText())
                self.append('\0')
                return
            self.sendSignal.emit(self.toPlainText())
            print('success press enter key', self.toPlainText())
class chatMsg(QThread):
    isSend_signal = pyqtSignal(tuple)
    recvSignal = pyqtSignal(tuple)
    sendSignal = pyqtSignal(tuple)
    def __init__(self, my_username, ta_username, socket, parent=None):
        super(chatMsg, self).__init__(parent)
        self.my_username = my_username
        self.ta_username = ta_username
        self.my_avatar = data.get_avatar(self.my_username)
        self.ta_avatar = data.get_avatar(self.ta_username)
        self.socket = socket
        self.my_port = self.search_port(my_username)
        self.ta_port = self.search_port(ta_username)
        self.ta_addr = ('localhost', self.ta_port) #todo 对方or服务器地址
    def update(self, my_username, ta_username, socket):
        self.my_username = my_username
        self.ta_username = ta_username
        self.my_avatar = data.get_avatar(self.my_username)
        self.ta_avatar = data.get_avatar(self.ta_username)
        self.socket = socket
        self.my_port = self.search_port(my_username)
        self.ta_port = self.search_port(ta_username)
        self.ta_addr = ('localhost', self.ta_port)
    def search_port(self, username):
        try:
            result=data.search_port(username)
            return result
        except:
            return None

    def send_msg(self, msg,type='U'):
        if type=='U':
            self.ta_port = self.search_port(self.ta_username)
            if self.ta_port is None:
                self.ta_port = 8000
            print('对方端口：', self.ta_port)
            self.ta_addr = ('localhost', self.ta_port)
            if self.ta_port == -1:
                print('对方不在线')
                return -1
            send_data = {
                'type': "U",
                'username': self.my_username,
                'content': msg
            }
            self.socket.sendto(json.dumps(send_data).encode('utf-8'), self.ta_addr)
            message = data.send_msg(
                IsSend=1,
                msg=msg,
                ta=self.ta_username,
                me=self.my_username,
                status=self.ta_port,
                _type=3,
            )
            self.sendSignal.emit(message)
            return message
        elif type=='G':
            gid = 123456 # todo 测试
            send_data = {
                'type': "G",
                'username': self.my_username,
                'content': msg,
                'gid': gid
            }
            ta_addr = ('localhost', 8000)
            self.socket.sendto(json.dumps(send_data).encode('utf-8'), ta_addr)
            message = data.send_msg(
                IsSend=1,
                msg=msg,
                ta=self.ta_username,
                me=self.my_username,
                status=self.ta_port,
                _type=3,
            )
            self.sendSignal.emit(message)
            return message
    # def run(self):
    #     # return
    #     messages = data.get_message(self.my_username, 0)
    #     # print(messages)
    #     for message in messages:
    #         self.isSend_signal.emit(message)

class recvThread(QThread):
    """
    接收消息线程
    """
    online_signal = pyqtSignal(str)
    recv_userSignal = pyqtSignal(tuple)
    recv_groupSignal = pyqtSignal(tuple)

    def __init__(self, my_u, socket, parent=None):
        super().__init__(parent)
        self.sec = 15  # 默认1000秒
        self.my_u = my_u
        self.my_avatar = data.get_avatar(self.my_u)
        self.socket = socket

    def run(self):
        while True:

            receive_data, client = self.socket.recvfrom(1024)
            msg = receive_data.decode('utf-8')
            recvmsg = json.loads(msg)
            ta_username = recvmsg['username']

            content = recvmsg['content']
            _type = recvmsg['type']
            print('收到数据：', ta_username, content)
            if content == '在线0000_1':
                self.online_signal.emit(ta_username)
                continue
            if _type == 'U':
                dt = datetime.datetime.now()
                message = (
                    0, 3, 0, dt, content, ta_username
                )
                data.send_msg(
                    IsSend=0,
                    msg=content,
                    ta=ta_username,
                    me=self.my_u,
                    status=1,
                    _type=3,
                )
                self.recv_userSignal.emit(message)
            elif _type == 'G':
                gid = recvmsg['gid']
                message = (
                    1, gid, _type, content, datetime.datetime.now(), ta_username, 0
                )
                self.recv_groupSignal.emit(message)
                pass
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWinController = MainWinController("avatar")
    mainWinController.show()
    sys.exit(app.exec_())
