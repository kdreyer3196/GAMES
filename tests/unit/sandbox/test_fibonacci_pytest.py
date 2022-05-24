#!/usr/bin/env python3

from sandbox.fibonacci import Fibonacci


def test_fibonacci_first_seven_pytest():
    n2expected = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8)]
    for n, expected in n2expected:
        assert Fibonacci().calculate(n) == expected
