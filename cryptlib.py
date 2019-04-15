from config import *

class Zip(object):

    def get(self,out_textname):
        zi=os.path.join(zip_path,out_textname)
        zipf = zipfile.ZipFile(zi, 'w')
        for (root_name, dirs_name, files_name) in os.walk(text_path):
            for filename in files_name:
                pathfile = os.path.join(text_path, filename)
                zipf.write(pathfile)
            zipf.close()
        t=time.strftime('%Y-%m-%d %X',time.localtime())
        print("打包完成，当前时间为",t)

    def lose(self,file_name):
        text_path = os.path.join(zip_path,file_name)
        unzip = zipfile.ZipFile(text_path, 'r')
        for file in unzip.namelist():
            unzip.extract(file, de_text_path)

class AES(object):

    def __init__(self,text_name,password=pwd):
        self.text=text_name
        self.password=pwd

    def encrypt(self):
        # 对称加密
        # TEXT是原文件
        path = os.path.join(text_path, self.text)
        out_path = os.path.join(en_text_path, self.text)
        os.system("openssl enc -aes-128-cbc -e -in %s -out %s -pass pass:%s"
                  %(path,out_path,self.password))
        if del_text==0:
            try:
                os.remove(path)     #删除源文件
            except FileNotFoundError:
                pass
        elif del_text==1:
            pass

    def decrypt(self):
        # 对称解密
        path = os.path.join(en_text_path, self.text)
        out_path = os.path.join(de_text_path, self.text)
        os.system("openssl enc -aes-128-cbc -d -in %s -out %s -pass pass:%s"
                    % (path, out_path, self.password))
        if del_text == 0:
            try:
                os.remove(path)  # 删除源文件
            except FileNotFoundError:
                pass
        elif del_text == 1:
            pass


class SHA1(object):
    # 计算sha1
    def __init__(self,name,path):
        self.filename=name
        self.path=path

    def cal(self):

        filename_file = os.path.join(self.path, self.filename)
        save_path=os.path.join(en_text_path,self.filename)
        a = os.popen("openssl dgst -sha1 %s" % filename_file).read()
        b = a[-41:]
        with open(save_path + ".sha1", "w",encoding='utf-8') as f:
            f.write(b)
        print("SHA1计算完成，当前时间为：", (time.strftime('%Y-%m-%d %X', time.localtime())))


    # 验证sh1
    def verify(self):

        filename_file = os.path.join(en_text_path, self.filename+'.sha1')
        flien=os.path.join(self.path,self.filename)
        a = os.popen("openssl dgst -sha1 " + flien).read()
        b = a[-41:]
        with open(filename_file, "r",encoding='utf-8') as f:
            B = f.read()
        if b == B:
            print("校验正确")
        else:
            print("校验错误，文件有可能被修改，5秒后删除该文件")
            time.sleep(5)
            os.remove(filename_file)
            os.remove(flien)
            print("删除成功！%s and %s"%(filename_file,flien))


class RSA(object):                      #非对称加密对称密码密钥文本

    def encrypt(self,name):

        try:
            (pubkey, privkey) = rsa.newkeys(2048)
            with open("./key/pubkey.key", "w+") as f1:
                f1.write(pubkey.save_pkcs1().decode())  # 公钥
            with open("./key/privkey.key", "w+") as f2:
                f2.write(privkey.save_pkcs1().decode())  # 私钥
            with open(name, "r+") as f3:
                message = f3.read()
            rsa_key_text = rsa.encrypt(message.encode(), pubkey)
            with open(r'./key/'+name, "wb") as f4:
                f4.write(rsa_key_text)
        except Exception as a:
            print(a)

    def decrypt(self,name):

        with open("./key/privkey.key", "r") as f2:
            priv_key =rsa.PrivateKey.load_pkcs1(f2.read().encode())
        with open("./key/"+name, "rb") as f3:
            mge = f3.read()
        un_rsa_key = rsa.decrypt(mge,priv_key).decode()
        with open("./detext/"+name,"w+") as f4:
            f4.write(un_rsa_key)


class Disi(object):

    def __init__(self,name,path):

        self.path=path
        self.name=os.path.join(self.path,name+'.sha1')       #sha1文件名
        self.sha=os.path.join(self.path,name+".sign")    #数字签名后保存的文件名

    def sign(self):
        #签名
        privkey = './key/privkey.key'  # 私钥

        with open(privkey, "r")as f1:
            priv_key = rsa.PrivateKey.load_pkcs1(f1.read().encode())

        with open(self.name,'r') as f:
            mess=f.read()

        reslut=rsa.sign(mess.encode(),priv_key,'SHA-1')
        with open(self.sha,'wb') as f:
            f.write(reslut)

    def verify(self):
        #验证
        pubkey = './key/pubkey.key'  # 公钥
        with open(pubkey,'r') as f1:
            pub_key = rsa.PublicKey.load_pkcs1(f1.read().encode())

        with open(self.name,'r') as f:
            mess=f.read()

        with open(self.sha,'rb') as f:
            sign=f.read()
        try:
            ver=rsa.verify(mess.encode(),sign,pub_key)
            print('验证成功,使用的哈希算法是：%s'%ver)
        except Exception as e:
            print(e)

#info_time=os.stat(__file__)
#a=time.localtime(info_time.st_mtime)
#t=time.strftime('%Y-%m-%d %X',time.localtime(info_time.st_mtime))
#print(t)
#测试例子
#a=AES('123.txt')
#a.decrypt()
#h=SHA1('pwd.txt',path='./')
#h.verify()
#r=RSA()
#r.encrypt('pwd.txt')

#d=Disi('pwd.txt',path='./entext/')
#d.sign()
#d.verify()



