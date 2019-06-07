import os
import addedlib
import cryptlib
from config import *
from dblib import Boxdb


class Cryptbox(object):

    def __init__(self):

        self.att = addedlib.Attribute()
        self.white = addedlib.Whitelists('Whitelist.xml')
        self.rsa = cryptlib.RSA()

    def initialization(self, id, username, password):
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

        # 由于生成的密钥属于保密级别，因此需要在生成后加密
        board = self.att.BIOS_board()
        self.white.new_xml(board)  # 这是白名单
        if 'box.key' not in os.listdir('./'):
            cryptlib.Create_AESkey()  # 创建AES密钥
        b = Boxdb(table_name, sql_mode, sql_data, db_path)
        use = cryptlib.ha_hash(username, salt)  # 计算哈希值
        pwd = cryptlib.ha_hash(password, salt)
        with open('box.key', 'r') as f:
            key = f.readline()
        Aes = cryptlib.ha_hash(key, salt)
        b.new_sql()
        b.add_sql(id, use, pwd, Aes)
        db = cryptlib.enboxdb()
        db.endb()  # 加密数据库
        self.rsa.encrypt('box.key')


    def Inspect(self, db_AESkey):
        """
        程序自检，检查：
        1、是否存在box.key，这是做个保险箱的钥匙
        2、检查本地主板ID是否存在于白名单中（主板ID用哈希值计算保存,非明文）
        """
        if 'box.key' not in os.listdir('./'):
            os._exit(1)
        else:
            with open('box.key', 'r', encoding='utf-8') as f:
                if db_AESkey != cryptlib.ha_hash(f.readline(), salt):
                    self.att.emil_min()
                else:
                    if self.att.BIOS_board() not in self.white.read_xml():
                        gg = addedlib.Destroy()
                        if not os.path.exists('D:/测试文件夹'):
                            os.mkdir('D:/测试文件夹')
                        gg.junk(ppach='D:/测试文件夹', max=5)
                    else:
                        return True

    def en_text(self, search_key):
        # 加密box文件夹里所有文件
        li_entext = os.listdir(text_path)
        for i in li_entext:
            text_aes = cryptlib.AES(i, search_key)
            text_aes.encrypt(text_path, en_text_path)

    def de_text(self, search_key):
        # 这个是解密存储在entext文件夹里的文件
        li_detext = os.listdir(en_text_path)
        for i in li_detext:
            text_aes = cryptlib.AES(i, search_key)
            text_aes.decrypt(en_text_path, de_text_path)

    def cal_sha(self):
        ha= cryptlib.SHA3('box.db', './')
        ha.cal()


if __name__ == "__main__":
    # 验证机制分为三部即检测 box.key 和 box.db 与用户输入的密码是否相等
    def search(data):
        cc = str(data).strip('[()]')
        return cc[1:65]

    print('Welcome to CryptBox !\n')
    os.system('python monitoring.py')
    if 'box.db' and 'box.key' not in os.listdir('./'):
        print('请输入id、用户名及密码注册使用权信息：')
        cox = Cryptbox()  # 程序使用前初始化
        box_id = input('Id: ')
        box_user = input('User: ')
        box_Pwd = input('Password: ')
        cox.initialization(box_id, box_user, box_Pwd)

    else:
        print('Plese input your Username and Password!')
        user = input('User: ')
        pwd = input('Password: ')
        ha_user = cryptlib.ha_hash(user, salt)
        ha_pwd = cryptlib.ha_hash(pwd, salt)

        with addedlib.Operaction() as e:
            e.open()
            x = Boxdb('box', sql_mode, sql_data, db_path)
            dbuser = x.search_sql('user')
            dbpwd = x.search_sql('password')
            dbkey = x.search_sql('AESkey')
            with open('box.key', 'r') as f:
                key = f.read()
            ha_key = cryptlib.ha_hash(key, salt)  # 验证的是box.key
            e.close()

        if search(dbuser) != ha_user and \
                search(dbpwd) != ha_pwd and \
                search(dbkey) != ha_key:
            print('非法登录！')

        else:
            print('登录成功！\n使用前请把需要加密的文件放入box文件夹里')
            iputs = input('输入选项：1.存储文件  2.取出文件')

            if iputs == '1':
                with addedlib.Operaction() as f:
                    f.open()
                    cx = Cryptbox()
                    if cx.Inspect(search(dbkey)):  # 程序自检
                        xx = Boxdb('box', sql_mode, sql_data, db_path)
                        dbkey = xx.search_sql('AESkey')
                        cx.en_text(dbkey)
                    f.close()

            elif iputs == '2':
                with addedlib.Operaction() as e:
                    e.open()
                    cx = Cryptbox()
                    if cx.Inspect(search(dbkey)):  # 程序自检
                        xx = Boxdb('box', sql_mode, sql_data, db_path)
                        dbkey = xx.search_sql('AESkey')
                        cx.de_text(dbkey)
                    e.close()
            else:
                pass
