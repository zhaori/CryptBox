# -*- coding: UTF-8 -*-
# 监控文件创建时间、访问时间、修改时间等，进一步加强文件及程序本身的安全性
# 计算好box.key、box.db及Whitelist.xml的哈希值，因为这三个文件非常关键

import os
import threading
import time
import addedlib

def get_hash(dbname):
    db = os.popen('openssl dgst -sha1 ' + dbname)
    db_sha1 = db.read()
    return db_sha1[-41:]

def file_hash():
    # 处理得到的hash值
    # 这是第一步计算相关文件的hash值
    with open('box_db.hash', 'w', encoding='utf-8') as f:
        f.write(str(get_hash('box.db')))

    with open('Whitelist.hash', 'w', encoding='utf-8') as f:
        f.write(str(get_hash('Whitelist.xml')))

    with open('box_key.hash', 'w', encoding='utf-8') as f:
        f.write(str(get_hash('box.key')))

def back():
    # 返回从文件里读取的值
    with open('box_db.hash', 'r', encoding='utf-8') as f:
        box_db = f.readline()

    with open('Whitelist.hash', 'r', encoding='utf-8') as f:
        whitelist = f.readline()

    with open('box_key.hash', 'r', encoding='utf-8') as f:
        box_key = f.readline()

    return box_db, whitelist, box_key

# 这是写入.log日志的内容
def thead_box_db_hash():
    fd = addedlib.Attribute()
    boxdb_log = fd.control('./', 'box.db')
    with open('boxdb.log', 'a+', encoding='utf-8') as f1:
        f1.write(str(boxdb_log) + '\n')
        time.sleep(0.1)

def thead_box_key_hash():
    fd = addedlib.Attribute()
    boxkey_log = fd.control('./', 'box.key')
    with open('boxkey.log', 'a+', encoding='utf-8') as f1:
        f1.write(str(boxkey_log) + '\n')
        time.sleep(0.1)

def thead_whitelist_hash():
    fd = addedlib.Attribute()
    whitelist_log = fd.control('./', 'Whitelist.xml')
    with open('whitelist.log', 'a+', encoding='utf-8') as f2:
        f2.write(str(whitelist_log) + '\n')
        time.sleep(0.1)

# 开始创建多线程
def thead_1():  # box.db
    while 1:
        box_db_hash, whitelist_hash, box_key_hash = back()
        if box_db_hash != str(get_hash('box.db')):
            print('线程1')
            thead1 = threading.Thread(target=thead_box_db_hash, )
            thead1.start()
            thead1.join()
            time.sleep(1)
        else:
            print('没问题1')


def thead_2():  # box.key
    while 1:
        box_db_hash, whitelist_hash, box_key_hash = back()
        if box_key_hash != str(get_hash('box.key')):
            print('线程2')
            thead2 = threading.Thread(target=thead_box_key_hash, )
            thead2.start()
            thead2.join()
            time.sleep(1)
        else:
            print('没问题2')


def thead_3():  # whitelist.xml
    while 1:
        box_db_hash, whitelist_hash, box_key_hash = back()
        if whitelist_hash != str(get_hash('Whitelist.xml')):
            print('线程3')
            thead3 = threading.Thread(target=thead_whitelist_hash, )
            thead3.start()
            thead3.join()
            time.sleep(1)
        else:
            print('没问题3')


if __name__ == '__main__':
    print('正在监视')
    if 'box.db' and 'box.key' and 'Whitelist.xml' in os.listdir('./'):
        file_hash()
        thead_list = [thead_1, thead_2, thead_3]
        theads = []

        for i in thead_list:
            at = threading.Thread(target=i, )
            at.start()
            theads.append(at)

        for i in theads:
            i.join()
    else:
        print('Error')