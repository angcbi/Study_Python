# -*- coding:utf-8 -*-
from urllib import request,parse
from http import cookiejar
import re

class ZH():
    def __init__(self):
        self.headers={
            'User-Agent':"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
        }
        self.url='http://www.zhihu.com/login/email'
        self.url1='http://www.zhihu.com/captcha.gif'
        self.data={
            'remember_me':'true',
            'email':'username',
            'password':'password'
        }

    def createOpener(self):
        head=[]
        for key,value in self.headers.items() :
            head.append((key,value))
        cj=cookiejar.CookieJar()
        pro=request.HTTPCookieProcessor(cj)
        opener=request.build_opener(pro)
        opener.addheaders=head
        return opener

    def getPage(self):
        opener=self.createOpener()
        res=opener.open(self.url)
        return res.read().decode('utf-8')

    def get_xsrf(self):
        pageCode=self.getPage()
        com=re.compile('<input type=".*?name="_xsrf.*?value="(.*?)"/>')
        result=com.findall(pageCode,re.S)
        return result[0].strip()
    def captcha(self):
        opener=self.createOpener()
        res=opener.open(self.url1)
        data=res.read()
        f=open(r'c:\caption.gif','wb')
        f.write(data)
        f.close()


    def login(self):
        self.captcha()
        self.data['_xsrf']=self.get_xsrf()
        self.data['captcha']=input('输入验证码:\n')
        data=parse.urlencode(self.data).encode()
        opener=self.createOpener()
        res=opener.open(self.url,data)
        return res.read().decode('utf-8')

    # def login(self):
    #     self.data['_xsrf']=self.get_xsrf()
    #     print(self.data)
    #     data=parse.urlencode(self.data).encode()
    #     req=request.Request(self.url,data,headers=self.headers)
    #     res=request.urlopen(req)
    #     return res.read().decode('utf-8')


zz=ZH()
print(zz.login())
