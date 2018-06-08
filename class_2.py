# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 09:27:19 2017

@author: omf
"""
class student():
    pass
class student2(object):
    def __init__(self,name='jie',score='100'):
        self.name=name
        self.score=score
    

a=student()
print(type(a))

a=student2('hello',100)
print(a.name,a.score)


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
        print('animal is runing... ')

class dog(animal):
    def run(self):
        print('dog is running...')
    def eat(self):
        print('dog meat')

class cat(animal):
    pass


a=dog()

print(a.run())





