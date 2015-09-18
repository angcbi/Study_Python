# -*- coding:utf-8 -*-

import requests
import re
import queue
import time

#http://www.109ys.com/forum.php?mod=post&action=reply&fid=40&tid=7488&infloat=yes&handlekey=reply&inajax=1&ajaxtarget=fwin_content_reply

class Movie():
    def __init__(self):
        self.pageIndex=1
        self.url='http://www.109ys.com/member.php?mod=logging&action=login'
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.q=queue.Queue()
        self.s=requests.Session()
        self.ss=set()


    def getPage(self):
        try:
            url='http://www.109ys.com/forum-40-'+str(self.pageIndex)+'.html'
            print('正在访问第%s页！' %self.pageIndex)
            r=self.s.get(url,headers=self.headers)
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
            print(u'哇哈哈，运气不错哦！获取到%s条记录'% self.q.qsize())
        else :
            print('未匹配到数据')
        self.pageIndex+=1

    def login(self):
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
            'username':'username',
            'password':'password',
            'formhas':formhash,
        }
        url='http://www.109ys.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash='+str(loginhash).upper()+'&inajax=1'
        print('正在登录...')
        r=self.s.post(url,data=data,headers=self.headers)
        if  re.search('欢迎您回来',r.text,re.S)==None:
            print('登录失败!')
        else:
            print('登录成功！')

    def replyTitle(self,title):
        url=title[1]
        url=re.sub('amp;','',url)
        r=self.s.get(url,headers=self.headers)
        formhash=re.findall('<input type=".*?name="formhash.*?value="(.*?)"',r.text,re.S)
        formhash=formhash[0]
        tid=re.search('tid=(.*?)&',url).group(1)
        print(title)
        replyurl='http://www.109ys.com/forum.php?mod=post&action=reply&replysubmit=yes&fid=40&tid='+str(tid)+'&inajax=1'+'&infloat=yes'
        data={
            'wysiwyg':'1',
            'noticeauthor':'',
            'noticetrimstr':'',
            'noticeauthormsg':'',
            'subject':'',
            'message':'谢谢分享，非常感谢，好的！'.encode('gbk'),
            'save':'',
            'posttime':str(int(time.time())),
            'formhash':formhash,
            'usesig':'1'
        }
        r=self.s.post(replyurl,data=data,headers=self.headers)
        r=self.s.get(url,headers=self.headers)
        # title=re.findall('<h1 class="ts">(.*?)<span id="thread.*?>(.*?)</span>.*?alt=.*?title=.*?:(.*?)" />',r.text,re.S)
        hot=re.findall(r'title="热度:(.*?)"',r.text,re.S)
        downloadlink=re.findall('<div class="showhide.*?href="(.*?)"',r.text,re.S)
        print('类型：%s\t热度:%s\n%s\n下载链接: %s' %(title[0].strip(),hot[0].strip(),title[2].strip(),downloadlink[0].strip()))
        # print('类型：%s\t热度:%s\n%s:' %(title[0].strip(),hot[0].strip(),title[2].strip()))

    def start(self):
        self.login()
        self.getItems()
        while self.q.qsize()>0 :
            title=self.q.get()
            if title not in self.ss:
                self.ss.add(title)
                time.sleep(16)
                self.replyTitle(title)
            # self.getItems()



m=Movie()
m.start()

