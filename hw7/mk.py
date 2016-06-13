#!/usr/bin/env python3

import sys
import csv
from itertools import combinations_with_replacement

def mk(x, y, p=1):

    return sum(abs((xi - yi)) ** p \
            for (xi, yi) in zip(x, y)) \
            ** (1 / p)

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename, 'r')
    reader = csv.reader(file)

    D = [[float(item) for item in row]
            for row in reader]

    for v1 in D:
        for v2 in D:
            dist = mk(v1, v2, p=3)
            print('{:.3}'.format(dist), end=',')
        print()

    
