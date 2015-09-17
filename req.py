# -*- coding:utf-8 -*-

import requests
import re
import queue


#
# http://www.109ys.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1
# http://www.109ys.com/forum.php?mod=forumdisplay&fid=40&page=4
# http://www.109ys.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=reply&loginhash=Lnz02&inajax=

#http://www.109ys.com/forum.php?mod=post&infloat=yes&action=reply&fid=40&extra=&tid=8449&replysubmit=yes&inajax=1

#http://www.109ys.com/forum.php?mod=post&action=reply&fid=40&tid=8449&infloat=yes&handlekey=reply&inajax=1&ajaxtarget=fwin_content_reply

#http://www.109ys.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=reply&loginhash=LCZvv&inajax=1

class Movie():
    def __init__(self):
        self.pageIndex=1
        self.loginUrl='http://www.109ys.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.q=queue.Queue()


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
        data={
        #     # 'mod':'logging',
        #     # 'action':'login',
        #     # 'loginsubmit':'yes',
        #     # 'infloat':'yes',
        #     # 'lssubmit':'yes',
        #     # 'inajax':'1',
        #     'fastloginfield':'username',
        #     'username':'xiaobeiwd',
        #     'cookietime':'2592000',
        #     'password':"jiang179660",
            'questionid':'0',
            'answer':'',
            'fastloginfield':'username',
            'cookietime':2592000,
            'quickforward':'yes',
            'handlekey':'ls',
            'username':'xiaobeiwd',
            'password':'jiang179660'
        }
        s=requests.Session()
        r=s.post(self.loginUrl,data,self.headers)
        print(r.text)


        # cj=cookiejar.CookieJar()
        # pro=request.HTTPCookieProcessor(cj)
        # opener=request.build_opener(pro)
        # request.install_opener(opener)
        # url='http://www.109ys.com/'+'member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        # data=parse.urlencode(data).encode()
        # print(url,data)
        # req=request.Request(self.loginUrl,data,self.headers)
        # res=request.urlopen(req)
        # print(res.read())




m=Movie()
m.login()



