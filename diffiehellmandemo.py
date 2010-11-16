#!/usr/bin/env python
# vim: set fileencoding=utf-8:
"""Read CrypTool Diffie-Hellman log file and compute A, B, SA, SB
"""

import fileinput

from cryptool_log import parse_cryptool_log
import diffiehellman

def main(inputfile):
    p, g, a, b, A, B, SA, SB = parse_cryptool_log(open(inputfile, 'r'))

    format ="""
    p: %s,
    g: %s,
    a: %s,
    b: %s,
    A: %s,
    B: %s,
    SA: %s,
    SB: %s."""

    try:
        alice = diffiehellman.DiffieHellman('alice', p, g)
        bob = diffiehellman.DiffieHellman('bob', p, g)

        alice.setSecret(a)
        bob.setSecret(b)

        computedA = alice.getPartialKey()
        computedB = bob.getPartialKey()

        alice.sendPartialKey(computedB)
        bob.sendPartialKey(computedA)

        computedSA = alice.getSecretKey()
        computedSB = bob.getSecretKey()

        print 'Eingelesene Werte:', format % (p, g, a, b, A, B, SA, SB)
        print "Berechnete Werte:",format % (p, g, a, b, computedA, computedB, computedSA, computedSB)
    except OverflowError, oe:
        import timeit
        x, y, z = oe.args[1]
        seconds = timeit.timeit('diffiehellman.naive_pow({0},{1},{2})'.format(x,100000,z),
            'import diffiehellman',number=1) / 100000.0

        error = """y ist zu groß.
    x hoch y mod z kann mit diesem Algorythmus nicht berechnet werden.
    Es würde {0} Jahre dauern.

    Lieber square-and-multiply benutzen""".format(y/(60*60*24*365)*seconds)
        print error
        exit()

def usage():
    print """Usage: python %s <algo> <CrypToolLog.txt>
    algo = naive | square-and-multiply""" % __file__
if __name__ == "__main__":
    import sys

    try:
        algo_str = sys.argv[1]
        filename = sys.argv[2]
        if algo_str == 'naive':
            diffiehellman.pow_ = diffiehellman.naive_pow
        elif algo_str == 'square-and-multiply':
            diffiehellman.pow_ = diffiehellman.square_and_multiply_pow
        else:
            raise
    except:
        usage()
        exit()

    main(filename)
