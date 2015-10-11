# -*- coding:utf-8 -*-
'''
login zhihu.com need cookie and post twice
'''


from  urllib import  request,parse
import http.cookiejar
import re
import time

hosturl = 'http://www.zhihu.com'
posturl = 'http://www.zhihu.com/login/email'
captcha_pre = 'http://www.zhihu.com/captcha.gif?r='

#set cookie
cj = http.cookiejar.CookieJar()
cookie_support = request.HTTPCookieProcessor(cj)
opener = request.build_opener(cookie_support,request.HTTPHandler)
request.install_opener(opener)

#get xsrf
h = request.urlopen(hosturl)
html = h.read().decode('utf-8')
com=re.compile('<input type=".*?name="_xsrf.*?value="(.*?)"/>')
result=com.findall(html,re.S)
xsrf=result[0].strip()
print(xsrf)

#get captcha
def get_captcha():
    captchaurl = captcha_pre + str(int(time.time() * 1000))
    print(captchaurl)
    data = request.urlopen(captchaurl).read()
    f = open(r'c:\captcha.jpg',"wb")
    f.write(data)
    f.close()
    captcha = input('captcha is: ')
    print(captcha)
    return captcha

#post data
def post_data(captcha,xsrf):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer' : 'http:www.zhihu.com'}
    postData = {'_xsrf' : xsrf,
                'password' : 'password',
                'captcha' : captcha,
                'email' : 'useranme',
                'remember_me' : 'true',
                }

    #request
    postData = parse.urlencode(postData).encode()
    print(postData)
    req = request.Request(posturl, postData, headers)
    res = request.urlopen(req)
    text = res.read().decode('utf-8')
    return text

#post it
captcha=get_captcha()
print(captcha)
text=post_data(captcha,xsrf)
print(text)

#post again
captcha=get_captcha()
print(captcha)
text=post_data(captcha,xsrf)
print(text)

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
            'Referer': 'http://www.zhihu.com/'
           }

req = request.Request(url='http://www.zhihu.com', headers=headers)
res = request.urlopen(req)

