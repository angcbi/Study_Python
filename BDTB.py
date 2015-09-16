# -*- coding:utf-8 -*-

# 暂存，正则表达式提取卤煮发言，
import re
from urllib import request

class Tool():
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB(object):
    def __init__(self,baseUrl,seeLZ):
        self.baseUrl=baseUrl
        self.seeLZ='?see_lz'+str(seeLZ)
        self.tool=Tool()

    def getPage(self,pageNum):
        try:
            url=self.baseUrl+self.seeLZ+'&pn'+str(pageNum)
            req=request.Request(url)
            res=request.urlopen(req)
            # print(res.read().decode('utf-8'))
            return res.read().decode('utf-8')
        except request.URLError  as e :
            if hasattr(e,"reason"):
                print('连接失败',e.reason)
                return None
    def getTitle(self):
        page=self.getPage(1)
        com=re.compile('<h3 class="core_title_txt.*?title=(.*?)style.*?</h3>')
        result=com.findall(page,re.S)
        if result :
            return result
        else:
            return None
    def getPageNum(self):
        page=self.getPage(1)
        com=re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>')
        result=com.findall(page,re.S)
        if result :
            return result[0].strip()
        else:
            return None
    def getContent(self,page):
        pattern=re.compile('<div id="post_content_.*?>(.*?)</div>')
        items=pattern.findall(page)
        print(self.tool.replace(items[1]))


baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
bdtb.getContent(bdtb.getPage(2))