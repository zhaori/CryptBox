from config import *

class Boxdb(object):

    def __init__(self):

        self.table=table_name
        self.mode=sql_mode
        self.sql=sql_data
        self.dbpath=db_path

    def new_sql(self):
        # 数据库创建、插入表
        #md是model.py里的模板
        count = sqlite3.connect(self.dbpath)
        con = count.cursor()
        con.execute(self.mode)
        con.close()
        print("Create a successfully")

    def add_sql(self, id, username, password):
        #增添数据
        add_data = {'id':id,"user": username, "password": ha_hash(password)}
        count = sqlite3.connect(self.dbpath)
        con = count.cursor()
        con.execute(self.sql,add_data) #1
        count.commit()
        con.close()
        print("add a successfully")

    def delete_sql(self, element):
        # 删除数据table,element
        connt = sqlite3.connect(self.dbpath)
        con = connt.cursor()
        con.execute("delete from " + self.table + " where "+ element)
        connt.commit()
        connt.close()
        print("delete a successfully")

    def search_sql(self, query):
        #查询数据
        connt=sqlite3.connect(self.dbpath)
        con=connt.cursor()
        sql_data=con.execute("select "+query+" from "+self.table)
        all_table=sql_data.fetchall()
        connt.close()
        print(all_table)



#d=Boxdb()
#d.new_data()
#d.add_sql('1','zzg','666666')
#d.search_sql('user')
#d.delete_sql('id=1')
