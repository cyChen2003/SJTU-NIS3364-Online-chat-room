from contact.add_contactUi import *
from data import data
import socket


class Myadmin():

    def __init__(self):
        self.port = 8000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 使用UDP套接字
        self.socket.bind(('localhost', self.port))


    def run(self):
        while True:
            try:
                # 当有客户端发送UDP数据报时，执行以下代码
                recv_data,client = self.socket.recvfrom(1024)
                msg = recv_data.decode('utf-8')
                recvmsg = json.loads(msg)
                ta_username = recvmsg['username']
                user_port = data.search_port(ta_username)
                content = recvmsg['content']
                _type = recvmsg['type']
                if _type  == "G":
                    gid = recvmsg['gid']
                    #获取群成员
                    memebers = data.get_group_members(gid)
                    for member in memebers:
                        #获取成员的端口号
                        port = data.search_port(member[0])
                        #发送消息
                        self.send_msg(port, recvmsg,user_port)
            except Exception as e:
                print(e)
                continue

    def send_msg(self, port, recvmsg,user_port):
        print(f"当前发送端口号为：,{port}")
        ta_addr = ('localhost', port)
        send_data = {
            'type': "G",
            'username': recvmsg['username'],
            'content': recvmsg['content'],
            'gid': recvmsg['gid'],
        }
        send_data = json.dumps(send_data)
        if port != user_port:
            self.socket.sendto(send_data.encode('utf-8'), ta_addr)
if __name__ == '__main__':
    myadmin = Myadmin()
    myadmin.run()
