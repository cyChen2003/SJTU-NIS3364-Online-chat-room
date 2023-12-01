import json
import pymysql
import random
import time
import hashlib
import datetime
import os
import shutil
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = open(BASE_DIR+ '/data/config.json', 'r')
config = json.loads(f.read())
username = config['username']
password = config['password']
database = config['database']
# 打开数据库连接t
db = pymysql.connect(
    host='localhost',
    user=username,
    password=password,
    database=database,
    autocommit=True
)
cursor = db.cursor()

def send_msg(IsSend, msg, ta, me, status=-1, _type=3):
    if status == -1:
        return False
    send = 'insert into message (type,isSend,createTime,content,talkerId,username) values(%s,%s,%s,%s,%s,%s)'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if _type == 3:
        cursor.execute(send, [_type, IsSend, dt, msg, ta, me])
        db.commit()
        return 1, _type, IsSend, datetime.datetime.now(), msg, ta