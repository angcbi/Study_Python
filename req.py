# -*- coding:gb2312 -*-
import requests

payload={
    'key1':'value1',
    'key2':'value2'
}

url='https://api.github.com/events'
r=requests.get(url,stream=True)

print(r.raw)
print(r.raw.read(10))

with open(r'c:\111','wb') as f:
    for chunk in r.iter_content(10):
        f.write(chunk)
