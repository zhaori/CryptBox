"""
简单地写了个关于sqlite数据库的增删查三种方法，有关表的创建，数据的插入配置均在
config.py文件里
"""

import sqlite3

from lib.cryptlib import ha_hash


class Boxdb(object):

    def __init__(self, table, mode, sql, path):
        self.table = table  # 表名
        self.mode = mode  # 插入表
        self.sql = sql  # 插入数据
        self.dbpath = path  # 数据库存储路径

    def new_sql(self):
        # 数据库创建、插入表
        # md是model.py里的模板
        with sqlite3.connect(self.dbpath) as con:
            con.execute(self.mode)

    def add_sql(self, id, username, password, AESkey):
        # 增添数据
        add_data = {'id': id, "user": username, "password": ha_hash(password), 'AESkey': AESkey}
        with sqlite3.connect(self.dbpath) as con:
            con.execute(self.sql, add_data)  # 1

    def delete_sql(self, element):
        # 删除数据table,element
        with sqlite3.connect(self.dbpath) as con:
            con.execute("delete from " + self.table + " where " + element)
            print("delete a successfully")

    def search_sql(self, query):
        # 查询数据
        with sqlite3.connect(self.dbpath) as con:
            sql_data = con.execute("select " + query + " from " + self.table)
            all_table = sql_data.fetchall()

        return all_table
# 37

