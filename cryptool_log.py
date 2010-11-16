#!/usr/bin/env python

import re
def parse_cryptool_log(input):
    """parse output of CrypTool's Diffie-Hellman demo (as open file) to a list of longs

    Examples of use:
    >>> log='''
    ... bla bla bla
    ... p: 1
    ... g: 2
    ... bla bla bla blaaa
    ... bla bla bla
    ... a: 3
    ... b: 4
    ... A: 5
    ... B: 6
    ... SA: 7
    ... SB: 8'''
    >>> parse_cryptool_log(line for line in log.splitlines())
    [1L, 2L, 3L, 4L, 5L, 6L, 7L, 8L]

    >>> parse_cryptool_log(open('Cry-cry2.txt'))
    [97L, 2L, 14L, 8L, 88L, 62L, 61L, 61L]

    >>> log='''
    ... bla bla bla
    ... p: 1
    ... g: 2
    ... A: 5
    ... B: 6
    ... SA: 7
    ... SB: 8'''
    >>> parse_cryptool_log(line for line in log.splitlines())
    Traceback (most recent call last):
    ...
    Exception: Could not parse CrypTool log, expected: A, got a


    """

    vars = ('p', 'g', 'a', 'b', 'A', 'B', 'SA', 'SB')
    pattern = re.compile(r'^(\w{1,2}): (\d*)\s*$')
    matches = (pattern.match(line) for line in input)
    groups = (m.groups() for m in matches if m)
    def gen_values():
        for (name, value), expected_name in zip(groups, vars):
            if name != expected_name:
                raise Exception('Could not parse CrypTool log, expected: {0}, '
                        'got {1}'.format(name, expected_name))
            yield long(value)
    return list(gen_values())
