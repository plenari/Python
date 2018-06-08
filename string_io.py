# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 11:05:17 2017
@author: shengjiex@qq.com
"""
from io import StringIO
f=StringIO()
#f.write('hello jie')
f = StringIO('Hello!\nHi!\nGoodbye!')

while True:
    s=f.readline()
    if s=='':
        break
    print(s.strip())
f.close()
        
#StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。
from io import BytesIO
f=BytesIO()
f.write('中文'.encode('utf-8'))
print(f.getvalue())
