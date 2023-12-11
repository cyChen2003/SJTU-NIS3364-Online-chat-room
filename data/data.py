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
def get_avatar(username):
    if username is None:
        username='avatar'
    sql = 'select avatar from user_info where username = %s'
    cursor.execute(sql, username)
    result = cursor.fetchone()
    return result[0]
def insert_user(username,password, avatar,port):
    sql = 'select * from user_info where username = %s'
    cursor.execute(sql, username)
    result = cursor.fetchone()
    #如果存在并且密码正确
    if result and result[2] != password:
        return False
    if result and result[2] == password:
        sql = 'update user_info set port = %s,online = 1 where username = %s'
        cursor.execute(sql, [port,username])
        db.commit()
        return True
    if result is None:
        print(type(username),type(password),type(avatar),type(port))
        sql = 'insert into user_info (username,avatar,pwd,port,online) values(%s,%s,%s,%s,%s,1)'
        cursor.execute(sql, [username, avatar,password, port])
        db.commit()
        return True
    return False
def search_port(username):
    if username is None:
        return False
    sql = 'select port from user_info where username = %s'
    cursor.execute(sql, username)
    result = cursor.fetchone()
    if result is None:
        return False
    return result[0]
def get_message(username, talkerId):
    if username is None or talkerId is None:
        return False
    sql = f'select * from message where talkerId = %s'
    cursor.execute(sql, [talkerId])
    result = cursor.fetchall()
    return result
def use_port_get_username(port,type="online"):
    if type=="online":
        sql = f'select username from user_info where port = %s and online = 1'
        cursor.execute(sql, [port])
        result = cursor.fetchone()
        if result is None:
            return False
    else:
        sql = f'select username,online from user_info where port = %s'
        cursor.execute(sql, [port])
        result = cursor.fetchone()
        if result is None:
            return 0,0
    return result[0],result[1]
def offline(username):
    sql = f"update user_info set online = 0 where username = %s"
    cursor.execute(sql, [username])
    db.commit()
    return True
def get_group_members(gid):
    sql = f"select username from group_members where gid = %s"
    cursor.execute(sql, [gid])
    result = cursor.fetchall()
    return result
def get_user_group(username):
    sql = f"select gid from group_members where username = %s"
    cursor.execute(sql, [username])
    result = cursor.fetchone()
    return result[0]
def join_group(username,gid):
    #判断是否已经加入
    sql = f"select * from group_members where gid = %s and username = %s"
    cursor.execute(sql, [gid,username])
    result = cursor.fetchone()
    if result:
        return True
    else:
        sql = f"insert into group_members (gid,username) values(%s,%s)"
        cursor.execute(sql, [gid,username])
        db.commit()
        return True
