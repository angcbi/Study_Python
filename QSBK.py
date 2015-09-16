#coding=utf-8

from  urllib import request,parse
import re

class QSBK():
    def __init__(self):
        self.pageIndex=1
        self.headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        self.stories=[]
        self.enable=True

    def getPage(self,pageIndex):
        try:
            url='http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            req=request.Request(url,headers=self.headers)
            res=request.urlopen(req)
            pagedata=res.read().decode('utf-8','ignore')
            return pagedata
        except request.URLError as e :
            if hasattr(e,"reason"):
                print('连接失败',e.reason)
            return None
    def getPageItems(self,pageIndex):
        pageCode=self.getPage(pageIndex)
        if not pageCode :
            print('页面加载失败')
            return None
        pattern=re.compile('<div class="author.*?target="_blank.*?src=.*?/>(.*?)</a>.*?<div class="content">(.*?)<!--(.*?)-->.*?<div class="stats">.*?<i class="number">(.*?)</i>',re.S)
        items=pattern.findall(pageCode)
        pageStories=[]
        for item in items:
            replaceBR=re.compile('<br/>')
            text=re.sub(replaceBR,'\n',item[1])
            pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
        return pageStories
    def loadPage(self):
        print('按任意键继续，按Q|q退出！')
        while self.enable :
            while len(self.stories)< 2 :
                pagestories=self.getPageItems(self.pageIndex)
                if pagestories :
                    self.stories.append(pagestories)
                    self.pageIndex+=1
            for onestory in self.stories[0]:
                aa=input()
                if aa.upper()=='Q' :
                    self.enable=False
                    break
                print('第%d页\t用户名: %s\t赞: %s\n%s' %(self.pageIndex-2,onestory[0],onestory[2],onestory[1]))
            else:
                print('退出成功！')
            del self.stories[0]

s=QSBK()
s.loadPage()

