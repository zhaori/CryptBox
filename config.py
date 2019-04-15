import os
import secrets
import rsa
import time
import zipfile
import hashlib
import sqlite3

#第三方库的第三方下载网址清华下载
#pi_url="https://pypi.tuna.tsinghua.edu.cn/simple"

#加入系统临时环境变量
os.system('path=%path%;./')

#文件路径
text_path = './box/'
en_text_path='./entext/'
de_text_path='./detext/'
zip_path='./zip'


#随机AES密码，如有必要也可以自己创建pwd.txt文件，里面存放你的密码
#nbyes只能小于等于180
try:
    with open('pwd.txt','r') as f:
        pwd=f.readline()
except FileNotFoundError:
    with open('pwd.txt','w') as f:
        f.write(str(secrets.token_urlsafe(nbytes=180)))


#加密文件后是否删除源文件，0为删除，1为保留
del_text=1

#数据库建表
sql_mode="""create table box(
                id  text,
                user text,
                password text
           )
        """
#数据库的表名，必须和上面的sql_mode保持一致
table_name='box'
#数据库保存路径
db_path=r"./box.db"

#插入数据
sql_data="""insert into box
        (id,user,password) 
        values
        (:id, :user, :password)"""


#salt即盐值，可自定义
salt="666666"
def ha_hash(password,salt=salt):
    data = password + salt
    text=hashlib.sha1(data.encode("utf8"))
    return text.hexdigest()



#短信发送参数配置

# 短信应用SDK AppID
appid = 1400200726  # SDK AppID是1400开头

# 短信应用SDK AppKey
appkey = "07a9ded4b423a6b17ab54dcace3a5f58"

# 需要发送短信的手机号码
phone_numbers = ["13568610410"]

# 短信模板ID，需要在短信应用中申请
template_id = 7839  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请

# 签名
sms_sign = "腾讯云"  # NOTE: 这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`