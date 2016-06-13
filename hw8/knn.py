#!/usr/bin/env python

from __future__ import division

import sys
import csv
import pprint
from collections import Counter

import tenfold

pprinter = pprint.PrettyPrinter()

def dist(x, y):
    return sum(abs(xi - yi) ** 2 \
            for (xi, yi) in zip(x, y)) \
            ** 0.5

def santinize(row):
    x = []
    for item in row[:-1]:
        x.append(float(item))
    x.append(row[-1].strip("'"))
    return x

class KNN:

    def __init__(self, Dc, k=3):
        self.k = k
        self.Dc = Dc
        self.D = [x[:-1] for x in Dc]
        self.classes = list(set(x[-1] for x in Dc))

    def test(self, Tc):
        print('Dc = {}'.format(Dc))
        print('Tc = {}'.format(Tc))
        err_cnt = 0
        for xc in Tc:
            x = xc[:-1]
            cls = xc[-1]
            result = self.test_one(x, cls)
            if not result:
                err_cnt += 1

        err_ratio = err_cnt / len(Tc)
        return err_ratio

    def test_one(self, x, cls):
        print('test one: {} of class "{}"'.format(x, cls))
        dists = []
        for yc in self.Dc:
            y = yc[:-1]
            c = yc[-1]
            d = dist(x, y)
            dists.append((y, c, d))

        dists.sort(key=lambda u: u[2])
        k = self.k
        voters = dists[:k] if k < len(dists) else dists
        pprinter.pprint(voters)
        counter = Counter(u[1] for u in voters)
        pred = sorted(counter.items(), 
                key=lambda v: v[1],
                reverse=True)[0][0]
        return pred == cls


if __name__ == '__main__':

    filename = sys.argv[1]
    file = open(filename, 'r')
    reader = csv.reader(file)

    Dc = [santinize(row) for row in reader]

    err_ratios = []
    for _ in range(5):
        tenfolds = tenfold.tenfold_expanded(Dc)
        for (one, others) in tenfolds:
            knn = KNN(others)
            err_ratio = knn.test(one)
            err_ratios.append(err_ratio)
            print('error ratio = {}'.format(err_ratio))

    avg_err_ratio = sum(err_ratios) / len(err_ratios)
    print('average error ratio = {}'.format(avg_err_ratio))


