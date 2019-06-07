"""
于2019/04/29完成，cryptlib封装的是与安全相关的功能包括，AES、RSA、SHA3、SHA256、签名验证等。
无论是AES还是RSA等等，都是只拥有加密、解密两种相反的方法

"""
import hashlib
import logging
import os
import secrets  # 注意这个Python自带的标准库不支持Python2.7
import shutil
import time
import zipfile

import rsa

from lib.config import *


class AES(object):
    """
    AES加密解密类,因为调用的是系统的openssl,因此下载它并添加到系统环境变量
    """

    def __init__(self, text_name, key):
        self.text = text_name
        self.password = key

    def encrypt(self, in_path, on_path):
        # 对称加密
        # TEXT是原文件
        path = os.path.join(in_path, self.text)
        out_path = os.path.join(on_path, self.text)
        try:
            os.system("openssl enc -aes-256-cbc -e -in %s -out %s -pass pass:%s"
                      % (path, out_path, self.password))
        except:
            logging.exception('Windows用户请手动安装openssl')
        finally:
            if del_text == 0:
                try:
                    os.remove(path)  # 删除源文件
                except FileNotFoundError:
                    pass
            elif del_text == 1:
                pass

    def decrypt(self, in_path, on_path):
        # 对称解密
        path = os.path.join(in_path, self.text)
        out_path = os.path.join(on_path, self.text)
        os.system("openssl enc -aes-256-cbc -d -in %s -out %s -pass pass:%s"
                  % (path, out_path, self.password))
        if del_text == 0:
            try:
                os.remove(path)  # 删除源文件
            except FileNotFoundError:
                pass
        elif del_text == 1:
            pass


class SHA3(object):
    """
    计算sha3  SHA1已经不安全了，而sha3只是说到目前为止尚未被攻破(2019/04/29)
    不过，即便是被攻破了，但这种破解的代价是极大的，以个人之力难以负担
    """

    def __init__(self, name, path):
        self.filename = name
        self.path = path

    def cal(self):
        filename_file = os.path.join(self.path, self.filename)
        save_path = os.path.join(en_text_path, self.filename + 'sha3')
        with open(filename_file, 'r') as f:
            hexdig = hashlib.sha3_256(str(f.read()).encode('utf8'))
        with open(save_path, 'w') as f:
            f.write(hexdig.hexdigest())

        print("SHA3计算完成，当前时间为：", (time.strftime('%Y-%m-%d %X', time.localtime())))

    # 验证sha
    def verify(self):
        filename_file = os.path.join(en_text_path, self.filename + '.sha3')
        flien = os.path.join(self.path, self.filename)
        with open(flien, 'r') as f:
            hexig = hashlib.sha3_256(str(f.read()).encode('utf8'))
            b = hexig.hexdigest()
        with open(filename_file, "r", encoding='utf-8') as f:
            B = f.read()
        if b == B:
            print("校验正确")
        else:
            print("校验错误，文件有可能被修改，5秒后删除该文件")
            time.sleep(5)
            os.remove(filename_file)
            os.remove(flien)
            print("删除成功！%s and %s" % (filename_file, flien))


class RSA(object):
    """
     非对称加密类,同样拥有加密解密的方法，公钥私钥是保存在key文件夹里的
     一定要注意私钥的安全
    """

    def encrypt(self, name):
        # if 'pubkey.key' and 'privkey.key' not in os.listdir('./key'):
        (pubkey, privkey) = rsa.newkeys(2048)
        with open("./key/pubkey.key", "w+") as f1:
            f1.write(pubkey.save_pkcs1().decode())  # 公钥

        with open("./key/privkey.key", "w+") as f2:
            f2.write(privkey.save_pkcs1().decode())  # 私钥

        with open(name, "r+") as f3:
            message = f3.read()

        rsa_key_text = rsa.encrypt(message.encode(), pubkey)
        key_file = os.path.join('./entext/', name)
        with open(key_file, "wb") as f4:
            f4.write(rsa_key_text)
        shutil.copy(key_file, './')
        os.remove(key_file)

    def decrypt(self, name):
        with open("./key/privkey.key", "r") as f2:
            priv_key = rsa.PrivateKey.load_pkcs1(f2.read().encode())

        with open(name, "rb") as f3:
            mge = f3.read()

        un_rsa_key = rsa.decrypt(mge, priv_key).decode()
        key_file = os.path.join('./entext/', name)
        with open(key_file, "w+") as f4:
            f4.write(un_rsa_key)

        shutil.copy(key_file, './')
        os.remove(key_file)


class Disi(object):
    """
    这是数字签名类，sign是签名，verify是验证，使用前必须保证文件已经加密结束
    私钥签名，公钥验证
    """

    def __init__(self, name, path):

        self.path = path
        self.name = os.path.join(self.path, name + '.sha3')  # sha1文件名
        self.sha = os.path.join(self.path, name + ".sign")  # 数字签名后保存的文件名

    def sign(self):
        # 签名
        privkey = './key/privkey.key'  # 私钥
        with open(privkey, "r")as f1:
            priv_key = rsa.PrivateKey.load_pkcs1(f1.read().encode())

        with open(self.name, 'r') as f:
            mess = f.read()

        reslut = rsa.sign(mess.encode(), priv_key, 'SHA-1')
        with open(self.sha, 'wb') as f:
            f.write(reslut)

    def verify(self):
        # 验证
        pubkey = './key/pubkey.key'  # 公钥
        with open(pubkey, 'r') as f1:
            pub_key = rsa.PublicKey.load_pkcs1(f1.read().encode())

        with open(self.name, 'r') as f:
            mess = f.read()

        with open(self.sha, 'rb') as f:
            sign = f.read()
        try:
            ver = rsa.verify(mess.encode(), sign, pub_key)
            print('验证成功,使用的哈希算法是：%s' % ver)
        except Exception as e:
            print(e)


def Create_AESkey():
    """
    随机AES密码,secrets这个库还有很多用处......
    用于程序初始化使用
    """
    if 'box.key' not in os.listdir('./'):
        with open('box.key', 'w') as f:
            pwd = str(secrets.token_urlsafe(nbytes=byes))
            f.write(pwd)
        return pwd
    else:
        pass


def ha_hash(password, salt=salt):
    """
    :param password: 不一定是密码，也可以是其它的字符串
    :param salt: 自定义盐，但从某种意义上说，这种固定盐不能称之为盐，依旧有很大的可能性被“撞上”
    :return: 计算哈希值
    """
    data = password + salt
    text = hashlib.sha256(data.encode("utf8"))
    return text.hexdigest()


class Zip(object):
    """
    打包文件夹,类似于Linux系统下的tar格式，只是打包为一个文件本身不压缩
    """

    def get(self, out_textname):
        zi = os.path.join(zip_path, out_textname)
        zipf = zipfile.ZipFile(zi, 'w')
        for (root_name, dirs_name, files_name) in os.walk(text_path):
            for filename in files_name:
                pathfile = os.path.join(text_path, filename)
                zipf.write(pathfile)
            zipf.close()
        t = time.strftime('%Y-%m-%d %X', time.localtime())
        print("打包完成，当前时间为", t)

    def lose(self, file_name):
        text_path = os.path.join(zip_path, file_name)
        unzip = zipfile.ZipFile(text_path, 'r')
        for file in unzip.namelist():
            unzip.extract(file, de_text_path)


class enboxdb(object):
    """
    用于加密数据库，在使用前加密，使用中解密，使用完再加密
    """

    def __init__(self):
        self.name = 'box.db'
        self.en = os.path.join('./entext', self.name)
        self.de = os.path.join('./detext', self.name)
        with open('box.key', 'r', encoding='utf-8') as f:
            key = f.readline()
        self.aes = AES('box.db', key)

    def endb(self):
        self.aes.encrypt('./', './entext/')
        shutil.copy(self.en, './')
        os.remove(self.en)

    def dedb(self):
        self.aes.decrypt('./', './detext')
        shutil.copy(self.de, './')
        os.remove(self.de)

# 168+150+113
