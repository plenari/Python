# -*- coding: utf-8 -*-


class Student(object):
    '''
    the class of studen which conclude name and score.
    
    >>> s1 = Student('Bart', 70)
    >>> s1.get_grade()
    'B'
    >>> s2 = Student('Bart', 700)
    >>> s2.get_grade()
    Traceback (most recent call last):
    ...
    ValueError: error input score
    '''
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def get_grade(self):
        if self.score > 100:
            raise ValueError("error input score")
        if self.score >= 80:
            return 'A'
        if self.score >= 60:
            return 'B'
        if self.score <0:
            raise ValueError("error input score")
        return 'C'
    
if __name__=='__main__':
    import doctest
    doctest.testmod()