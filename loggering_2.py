# -*- coding: utf-8 -*-

import logging
import sys

# 获取logger实例，如果参数为空则返回root logger
#默认的logger名称是root
logger = logging.getLogger("test")
#往里添加处理器

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

# 文件日志
#最常用的是StreamHandler和FileHandler, Handler用于向不同的输出端打log。
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)

# 输出不同级别的log
logger.debug('this is debug info')
logger.info('this is information')
logger.warning('this is warning message')
logger.error('this is error message')
logger.fatal('this is fatal message, it is same as logger.critical')
logger.critical('this is critical message')

try:
    1 / 0
except:
    # 等同于error级别，但是会额外记录当前抛出的异常堆栈信息
    logger.exception('this is an exception message')
 
# 移除一些日志处理器
#如果不停的向logger 添加file_handler 会保存多分
logger.removeHandler(file_handler)


'''
第一坑
import logging
#这里会创建一个默认的handler
logging.basicConfig(level=logging.DEBUG)

fmt = '%(levelname)s:%(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(fmt))
#这里会在创建一个handler
logging.getLogger().addHandler(console_handler)

logging.info('hello!')

# INFO:root:hello!
# INFO:hello!
'''






