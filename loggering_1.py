# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 09:43:12 2017
@author: shengjiex@qq.com
是启动Python的调试器pdb，让程序以单步方式运行
"""
import logging

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)

logging.debug('debug message')
logging.info('info message')
logging.warning('warn message')
logging.error('error message')
logging.critical('critical message')

'''
几个重要的概念

Logger 记录器，暴露了应用程序代码能直接使用的接口。
Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地。
Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录。
Formatter 格式化器，指明了最终输出中日志记录的布局。

'''
