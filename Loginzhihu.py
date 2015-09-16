# -*- coding:utf-8 -*-
from urllib import request,parse
from http import cookiejar
import re
import time


class ZH():
    def __init__(self):
        self.headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
            'Referer': 'http://www.zhihu.com/'
        }
        self.loginUrl='http://www.zhihu.com/login/email'
        self.captchaUrl='http://www.zhihu.com/captcha.gif?r='+str(int(time.time()*1000))
        self.indexUrl='http://www.zhihu.com/people/angcbi/'
        self.data={
            'remember_me':'true',
            'email':'useranme',
            'password':'password'
        }
        self.cj=cookiejar.CookieJar()
        self.opener=request.build_opener(request.HTTPCookieProcessor(self.cj))
        request.install_opener(self.opener)

    def getPage(self):
        req=request.Request(self.loginUrl,headers=self.headers)
        res=request.urlopen(req)
        return res.read().decode('utf-8')

    def getindexPage(self):
        req=request.Request(self.indexUrl,headers=self.headers)
        res=request.urlopen(req)
        return res.read()

    def get_xsrf(self):
        pageCode=self.getPage()
        com=re.compile('<input type=".*?name="_xsrf.*?value="(.*?)"/>')
        result=com.findall(pageCode,re.S)
        return result[0].strip()

    def captcha(self):
        req=request.Request(self.captchaUrl,headers=self.headers)
        res=request.urlopen(req)
        data=res.read()
        f=open(r'c:\caption.gif','wb')
        f.write(data)
        f.close()


    def login(self):
        self.captcha()
        self.data['_xsrf']=self.get_xsrf()
        self.data['captcha']=input(u'输入验证码:\n')
        data=parse.urlencode(self.data).encode()
        print(data)
        req=request.Request(self.loginUrl,data,self.headers)
        res=request.urlopen(req)
        return res.read()
    def start(self):
        print(self.login())
        print(self.login())
        print(self.getindexPage().decode('utf-8'))
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
zz=ZH()
zz.start()


