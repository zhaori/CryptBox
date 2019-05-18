import os
from config import *
import cryptlib
from dblib import Boxdb
import addedlib
import time

class Cryptbox(object):

    def __init__(self):

        self.att=addedlib.Attribute()
        self.white=addedlib.Whitelists('Whitelist.xml')
        self.rsa=cryptlib.RSA()

    def initialization(self,id,username,password):
        """
        程序运行初始化，文件夹、生成白名单和保险箱密钥及用户注册信息
        """
        began_time=time.time()
        if not os.path.exists('box'):
            os.mkdir('box')
        if not os.path.exists('detext'):
            os.mkdir('detext')
        if not os.path.exists('entext'):
            os.mkdir('entext')
        if not os.path.exists('key'):
            os.mkdir('key')
        if not os.path.exists('zip'):
            os.mkdir('zip')

        #由于生成的密钥属于保密级别，因此需要在生成后加密
        board=self.att.BIOS_board()
        self.white.new_xml(board)           #这是白名单
        if 'box.key' not in os.listdir('./'):
            cryptlib.Create_AESkey()                     # 创建AES密钥
        b=Boxdb(table_name,sql_mode,sql_data,db_path)
        use=cryptlib.ha_hash(username,salt)         #计算哈希值
        pwd=cryptlib.ha_hash(password,salt)
        with open('box.key', 'r', encoding='utf-8') as f:
                key=f.readline()
        Aes=cryptlib.ha_hash(key,salt)
        b.new_sql()
        b.add_sql(id,use,pwd,Aes)
        db = cryptlib.enboxdb()
        db.endb()                            #加密数据库
        self.rsa.encrypt('box.key')


    def use_login(self):
        #返回的是从数据库里读取的AES密钥,但这个密钥是经过RSA算法加密后的，如要使用还需解密
        db = cryptlib.enboxdb()
        db.dedb()
        b = Boxdb('box',sql_mode,sql_data,db_path)
        db_aes=b.search_sql('AESkey')
        li = []
        li.append(str(db_aes))
        l_key = ''.join(li).strip('[()]')
        db_AESkey=l_key[:-1].strip("''")
        return db_AESkey


    def Inspect(self,db_AESkey):
        """
        程序自检，检查1、是否存在box.key这是做个保险箱的钥匙
        2、检查本地主板ID是否存在于白名单中
        """
        if 'box.key' not in os.listdir('./'):
            os._exit(1)
        else:
            with open('box.key','r',encoding='utf-8') as f:
                if db_AESkey != cryptlib.ha_hash(f.readline(),salt):
                    self.att.emil_min()
                else:
                    if self.att.BIOS_board() not in self.white.read_xml():
                        gg=addedlib.Destroy()
                        gg.junk(ppach='D:/测试文件夹',max=50)
                    else:
                        self.rsa.encrypt('box.key')
                        return True


    def open_box(self,text,key):
        aes=cryptlib.AES(text,key)
        aes.encrypt(text_path,en_text_path)
        self.rsa.encrypt('box.key')

    def close_box(self,text,key):
        aes=cryptlib.AES(text,key)
        aes.decrypt(en_text_path,de_text_path)
        rsa=cryptlib.RSA()
        rsa.decrypt('box.key')


if __name__ == "__main__":

    print('Welcome to CryptBox !\n'
          'plese input your option')
    cox = Cryptbox()  # 程序使用前初始化
    cox.initialization('1', 'zg', '666666')
    print('1.将文件放入保险箱   2.取出文件')
    x = input('请输入选项：')
    if x == '1':
        cox.initialization('1', 'zg', '666666')
        rsa = cryptlib.RSA()
        rsa.decrypt('box.key')
        de_key = cox.use_login()
        cox.Inspect(de_key)
    #with open('box.key','r',encoding='utf-8') as f:
    #    key=f.readline()
    #cox.open_box('1.txt',key=key)
