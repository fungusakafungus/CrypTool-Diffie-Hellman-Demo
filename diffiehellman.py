#!/usr/bin/env python

def naive_pow(x, y, z):
    """x to power of y modulo z
    Ex.: 2**10 = 1024, 1024 mod 100 = 24
    >>> naive_pow(2,10,100)
    24

    >>> naive_pow(2,10000000000000000000000000000,100)
    Traceback (most recent call last):
    ...
    OverflowError: ('y too big', (2, 10000000000000000000000000000L, 100))
    """
    res = 1
    i = 0
    try:
        for i in xrange(y):
            res = res * x % z
    except OverflowError:
        raise OverflowError('y too big', (x, y, z))
    return res

def square_and_multiply_pow(x, y, z):
    """x to power of y modulo z, use square-and-multiply
    Ex.: 2**10 = 1024, 1024 mod 100 = 24
    >>> square_and_multiply_pow(2,10,100)
    24
    >>> square_and_multiply_pow(2,10000000000000000000000000000,100)
    76
    """
    res = 1
    bits = bin(y).lstrip('0b') # string, like '10011'
    for bit in bits:
        res = res * res % z # square
        if bit == '1':
            res = res * x % z # multiply
    return res

pow_ = naive_pow

class DiffieHellman(object):
    def __init__(self, name, p, g):
        self.name = name
        self.p = p
        self.g = g

    def setSecret(self, a):
        self.a = a % self.p

    def getPartialKey(self):
        return pow_(self.g, self.a, self.p) # g**a mod p

    def sendPartialKey(self, B):
        self.B = B % self.p

    def getSecretKey(self):
        return pow_(self.B, self.a, self.p)

