# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 11:05:17 2017
@author: shengjiex@qq.com
encode 编码||decode 解码||encoding 格式
>>> the help about open?
open(file, mode='r', buffering=-1, encoding=None, \
     errors=None, newline=None, closefd=True, opener=None)
"""

test_str='胜杰open file'
save=r'coding.txt'
with open(save,'w',encoding='utf-8') as f:
    f.write(test_str)
    
with open(save,'r',encoding='gbk') as f:    
    print('encode by utf-8,decode by gbk : ',f.read())
    
#字符的编码
gbk_str=test_str.encode('gbk')
""">>>b'\xca\xa4\xbd\xdcopen file'"""
#字符的解码，错误
try:
    gbk_str.decode('utf-8')
except:
    pass
""">>>'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte"""
#字符的解码,正确
gbk_str.decode('gbk')
""">>>'胜杰open file'"""
