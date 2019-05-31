"""
第三方库的第三方下载网址清华下载
lib_url="https://pypi.tuna.tsinghua.edu.cn/simple"
这是整个程序的配置文件，但有关数据库的配置部分，假如程序已经转换成可执行文件的话不建议修改
邮件的内容可以自定义为html
"""

# 文件路径
text_path = './box/'
en_text_path = './entext/'
de_text_path = './detext/'
zip_path = './zip'

# 随机AES密码，如有必要也可以自己创建box.key文件，里面存放你的密码
# byes只能小于等于180
byes = 180

# 加密文件后是否删除源文件，0为删除，1为保留
del_text = 1

# 数据库建表
sql_mode = """create table box(
                id  text,
                user text,
                password text,
                AESkey  text
           )
        """

# 数据库的表名，必须和上面的sql_mode保持一致
table_name = 'box'

# 数据库保存路径
db_path = r"./box.db"

# 插入数据
sql_data = """insert into box
              (id, user, password, AESkey) 
              values
              (:id, :user, :password, :AESkey)"""

# salt即盐值，可自定义
# 数据库存储密码

salt = "666666"

# 邮箱配置参数信息
# QQ接收邮件服务器：pop.qq.com,995
# 发送邮件服务器：smtp.qq.com,465、587

# 服务器地址
email_id = "smtp.qq.com"

# 服务器端口
email_port = "465"

# 发件邮箱
email_from = "1471584500@qq.com"

# 发件邮箱密码(授权码)不是邮箱密码
email_pwd = "lvaqtvpmpcnmgfah"

# 收件邮箱
email_to = "2134034899@qq.com"

# 邮件主题
subject = "安全提醒"

# 邮件内容
content = '''
    <center>
        <span style="font-size:30px;color:black">警告：程序非法使用</span>
    </center>            
'''

# 删除目录
path = r'D:/测试文件夹'
#33
