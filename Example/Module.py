#coding=utf8
import time
import random
import doctest
import unittest
import types


def test_generator(num):
    for x in xrange(num):
        yield x

def Add(a,b):
    return a + b

class TestAddMethod(unittest.TestCase):
    def test_Add(self):
        for x in xrange(10):
            for y in xrange(10):
                result = Add(x,y)
                self.failUnless((x + y) == result,'test add failed.')

if __name__ == '__main__':
    #unittest.main()

    num = 1 + 1j

    print num.real,num.imag,num.conjugate()

    print 1.0 / 2