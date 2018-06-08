# -*- coding: utf-8 -*-
"""
Created on Mon Dec 2018年3月25日
@author:shengjiex@qq.com
"""

import logging
logger = logging.getLogger("class")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler("class.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
"""
python class 内置属性
__dict__ : 类的属性（包含一个字典，由类的数据属性组成）
__doc__ :类的文档字符串
__name__: 类名
__module__: 类定义所在的模块（类的全名是'__main__.className'，如果类位于一个导入模块mymod中，那么className.__module__ 等于 mymod）
__bases__ : 类的所有父类构成元素（包含了一个由所有父类组成的元组）
"""

class Employee:
   
   '''
   所有员工的基类
   >>> Employee.__doc__
   所有员工的基类
   '''
   empCount = 0 
   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
     logger.info("Total Employee %d" % Employee.empCount)
 
   def displayEmployee(self):
      logger.info("Name : ", self.name,  ", Salary: ", self.salary)
 
logger.info("Employee.__doc__:{}".format( Employee.__doc__))
logger.info("Employee.__name__:{}".format(Employee.__name__))
logger.info("Employee.__module__:{}".format(Employee.__module__))
logger.info("Employee.__bases__:{}".format(Employee.__bases__))
logger.info("Employee.__dict__:{}".format(Employee.__dict__))


class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'
        
        
#base class super class
class animal(object):
    def __init__(self):
        pass
    def run(self):
        logger.info('animal is runing... ')

class dog(animal):
    def run(self):
        logger.info('dog is running...')
    def eat(self):
        logger.info('dog meat')

class cat(animal):
    pass

a=dog()

#logger.info(a.run())



# class A(object): python2 必须显示地继承object
class A:
    def __init__(self):
        print("__init__ ")
        super(A, self).__init__()

    def __new__(cls):
        print("__new__ ")
        return super(A, cls).__new__(cls)

    def __call__(self):  # 可以定义任意参数
        print('__call__ ')

    def __str__(self):
        print('__str__')


logger.removeHandler(file_handler)
