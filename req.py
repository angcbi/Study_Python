# -*- coding:utf-8 -*-

import requests
import re
import queue



class Movie():
    def __init__(self):
        self.pageIndex=1
        self.url='http://www.109ys.com/member.php?mod=logging&action=login'
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.q=queue.Queue()
        self.s=None


    def getPage(self):
        try:
            url='http://www.109ys.com/forum-40-'+str(self.pageIndex)+'.html'
            print('正在访问第%d页，网址：%s' %(self.pageIndex,url))
            s=requests.Session()
            r=s.get(url,headers=self.headers)
            return r.text
        except requests.HTTPError as e:
            print(e.errno,e.strerror)
            return None
    def getItems(self):
        data=self.getPage()
        com=re.compile('<em>\[<a href=".*?>(.*?)</a>\]</em>\s+<a href="(.*?)".*?s xst">(.*?)</a>')
        results=com.findall(data,re.S)
        if  results:
            for item in results:
                self.q.put(item)
            print('哇哈哈，不错哦！获取到%s条记录'% self.q.qsize())
        else :
            print('未匹配到数据')
        self.pageIndex+=1

    def login(self):
        self.s=requests.Session()
        r=self.s.get(self.url,headers=self.headers)
        loginhash=re.findall('loginhash=(.*?)"',r.text,re.S)
        formhash=re.findall('<input type=".*?name="formhash.*?value="(.*?)"',r.text,re.S)
        loginhash=loginhash[0]
        formhash=formhash[0]
        data={
            'questionid':'0',
            'answer':'',
            'loginfield':'username',
            'cookietime':2592000,
            'username':'xiaobeiwd',
            'password':'jiang179660',
            'formhas':formhash,
            'referer':'http://www.109ys.com/./'
        }
        url='http://www.109ys.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash='+str(loginhash).upper()+'&inajax=1'
        print('正在登录...')
        r=self.s.post(url,data=data,headers=self.headers)
        if  re.search('欢迎您回来',r.text,re.S)==None:
            print('登录失败!')
        else:
            print('登录成功！')
        return self.s
    def replyTitle(self,url):

m=Movie()
m.login()



