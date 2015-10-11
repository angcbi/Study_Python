# -*- coding:utf-8 -*-
'''
    Download images from http://qiubaichengren.com/
    Default save to c:\qsbk
'''

import requests
import time
import re
import os
import threading
import sys


def getCurrentTime():
    return time.strftime('[%y-%m-%d %H:%M:%S]',time.localtime(time.time()))


def getPage(pageNum):
    url='http://qiubaichengren.com/'+str(pageNum)+'.html'
    try:
        r=requests.get(url)
        r.encoding='gbk'
        return r.text
    except requests.HTTPError as e:
        print('连接失败： ',e)
        return None

def getItems(page):
    parrent=re.compile('<img alt="(.*?)" src="(.*?)"',re.S)
    items=re.findall(parrent,page)
    results=[]
    for item in items:
        results.append((item[0]+'.'+item[1].split('.')[-1],item[1]))
    return results

def downlowdImgae(results,path=r'c:\qsbk'):
    if not os.path.exists(path):
        os.mkdir(path)
        f_hd=open(os.path.join(path,'out.log'),'w')
        sys.stdout=f_hd
    for item in results:
        try:
            url=item[1]
            r=requests.get(url,stream=True)
            with open(os.path.join(path,item[0]),'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
                    f.flush()
            f.close()
            print('%s 下载 %s 成功！' % (getCurrentTime(),os.path.join(path,item[0])))

        except requests.HTTPError as e:
            print('下载失败',e)

def start(pageNum,step,path=r'd:\qsbk'):

    for pageNum in range(pageNum,pageNum+step+1):
        gP=threading.Thread(target=getPage,args=(pageNum,))
        gP.start()
        gP.join()
        gI=threading.Thread(target=getItems,args=(getPage(pageNum),))
        gI.start()
        gI.join()
        dI=threading.Thread(target=downlowdImgae,args=(getItems(getPage(pageNum)),path,))
        dI.start()
        dI.join()




start(1,30)