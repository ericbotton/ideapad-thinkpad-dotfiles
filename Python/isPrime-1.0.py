#!/usr/bin/env python

import sys
import math

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

def find_closest_prime(n):
    i = 1

    while True:
        if is_prime(n - i):
            return n - i
        elif is_prime(n + i):
            return n + i

        i += 1

if __name__ == '__main__':
    n = int(sys.argv[1])

    if is_prime(n):
        print("Prime")
    else:
        print(find_closest_prime(n))
