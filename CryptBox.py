import os
from config import *
import cryptlib
from dblib import Boxdb
import addedlib


class Cryptbox(object):

    def __init__(self):

        self.att=addedlib.Attribute()
        self.white=addedlib.Whitelists('Whitelist.xml')
        self.rsa=cryptlib.RSA()

    def initialization(self,id,username,password):
        """
        程序运行初始化，文件夹、生成白名单和保险箱密钥及用户注册信息
        """
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
        with open('box.key', 'r') as f:
                key=f.readline()
        Aes=cryptlib.ha_hash(key,salt)
        b.new_sql()
        b.add_sql(id,use,pwd,Aes)
        db = cryptlib.enboxdb()
        db.endb()                            #加密数据库
        self.rsa.encrypt('box.key')


    def use_login(self,data):
        #登录信息缓存
        pass

    def Inspect(self, db_AESkey):
        """
        程序自检，检查：
        1、是否存在box.key，这是做个保险箱的钥匙
        2、检查本地主板ID是否存在于白名单中（主板ID用哈希值计算保存,非明文）
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


if __name__ == "__main__":
    #验证机制分为三部即检测 box.key 和 box.db 与用户输入的密码是否相等

    cox = Cryptbox()  # 程序使用前初始化
    print('Welcome to CryptBox !\n')
    if 'box.db' and 'box.key' not in os.listdir('./'):
        print('请输入id、用户名及密码注册使用权信息：')
        box_id=input('Id: ')
        box_user=input('User: ')
        box_Pwd=input('Password: ')
        cox.initialization(box_id, box_user, box_Pwd)


    else:
        print('Plese input your Password!')
        pwd=input('Password: ')
        ha_pwd=cryptlib.ha_hash(pwd,salt)

        def search(data):
            cc = str(data).strip('[()]')
            return cc[1:65]

        with addedlib.Operaction() as e:
            e.open()
            x=Boxdb('box', sql_mode, sql_data, db_path)
            dbpwd=x.search_sql('password')
            dbkey=x.search_sql('AESkey')
            with open('box.key','r') as f:
                key=f.read()
            ha_key=cryptlib.ha_hash(key,salt)       #验证的是box.key
            e.close()

        if search(dbpwd) != ha_pwd :
            print('非法登录')
        else:
            print('登录成功')





