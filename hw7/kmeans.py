#!/usr/bin/env python

import sys
import csv
import argparse
import random
from itertools import combinations
import pprint
from matplotlib import pyplot as plt

pprinter = pprint.PrettyPrinter()

def dist(x, y):
    return sum(abs(xi - yi) ** 2 \
            for (xi, yi) in zip(x, y)) \
            ** 0.5

class Cluster(set):

    def __init__(self, D):
        self.D = D

    def avg(self):
        dists = [dist(self.D[xi1], self.D[xi2]) for (xi1, xi2) in combinations(self, 2)]
        avg = sum(dists) / len(dists)
        #print('avg({}) = {}'.format(self, avg))
        return avg

    def diam(self):
        diam = max(dist(self.D[xi1], self.D[xi2]) for (xi1, xi2) in combinations(self, 2))
        #print('diam({}) = {}'.format(self, diam))
        return diam

    def dmin(self, other):
        if not isinstance(other, Cluster):
            raise TypeError('dmin must take two Cluster')
        dmin = min(dist(self.D[xi], other.D[yi]) for xi in self for yi in other)
        #print('dmin({}) = {}'.format(self, dmin))
        return dmin

    def dcen(self, other):
        if not isinstance(other, Cluster):
            raise TypeError('dcen must take two Clusters')
        dcen = dist(self.mean(), other.mean())
        #print('dcen({}) = {}'.format(self, dcen))
        return dcen

    def mean(self):
        xs = [self.D[xi] for xi in self]
        return [sum(xis) / len(xis) for xis in zip(*xs)]

def dbi(clusters):

    def db(ci, cj):
        return (ci.avg() + cj.avg()) / ci.dcen(cj)

    def _(ci):
        return max(db(ci, cj) for cj in clusters if cj != ci)

    return sum(_(ci) for ci in clusters) / len(clusters)

def di(clusters):

    def dunn(ci, cj):
        return ci.dmin(cj) / max(cx.diam() for cx in clusters)

    def _(ci):
        return min(dunn(ci, cj) for cj in clusters if cj != ci)

    return min(_(ci) for ci in clusters)

class KMeans:

    def __init__(self, D):
        self.D = D

    def min_dist_index(self, x, mus):
        dists = [dist(x, mu) for mu in mus]
        min_dist = min(dists)
        min_index = dists.index(min_dist)
        return min_index

    def mean(self, xi_set):
        xs = [self.D[xi] for xi in xi_set]
        mean = [sum(xis) / len(xis) for xis in zip(*xs)]
        return mean

    def vector_equals(self, x, y):
        return all(xi == yi for (xi, yi) in zip(x, y))

    def kmeans(self, k=3):
        # initialize mean vector
        muis = random.sample(range(len(self.D)), k)
        #muis = [0, 1, 2, 3]
        mus = [self.D[i] for i in muis]

        rounds = 0
        while True:
            #print('==== new round =========')
            rounds += 1
            #print('mus = {}'.format(mus))
            clusters = [Cluster(self.D) for _ in mus]
            for xi, x in enumerate(self.D):
                mui = self.min_dist_index(x, mus)
                mu = mus[mui]
                clusters[mui].add(xi)
            #pprinter.pprint(clusters)
            new_mus = [cluster.mean() for cluster in clusters]
            if self.vector_equals(new_mus, mus):
                print('after {} rounds, no longer updates'.format(rounds))
                return mus, clusters
            else:
                #print('update mus, new_mus = {}'.format(new_mus))
                mus = new_mus

def kmeans(args):
    def sant_watermelon(row):
        x = []
        for item in row[:-1]:
            x.append(float(item))
        x.append(row[-1])
        return x

    filename = args.datafile
    file = open(filename, 'r')
    reader = csv.reader(file)
    D_ = [sant_watermelon(row) for row in reader]
    D = [x[:-1] for x in D_]  # eliminate class label
    classes = list(set(x[-1] for x in D_))
    print('classes = {}'.format(classes))
    k = len(classes) * args.multiple
    km = KMeans(D)
    mus, clusters = km.kmeans(k=k)

    pprinter.pprint(clusters)

    for cluster in clusters:
#        print cluster, ':'
#        for xi in cluster:
#            x = D[xi]
#            pprinter.pprint(x)
        avg = cluster.avg()
        diam = cluster.diam()
        break

    dbi_ = dbi(clusters)
    di_ = di(clusters)
    print('dbi = {}'.format(dbi_))
    print('di = {}'.format(di_))

    if args.plot:

        colors = ['#000000', '#0000ff', '#66ff00', '#ff3300', '#00dddd', '#ff00ff']
        markers = ['o', '^', '4', '*', 'd', 's']

        for i, cluster in enumerate(clusters):
            color = colors[i % len(colors)]
            for xi in cluster:
                x = D_[xi]
                j = classes.index(x[-1])
                #print 'j =', j
                marker = markers[j]
                plt.scatter(*x[:-1], marker=marker, color=color)


        for mu in mus:
            plt.scatter(*mu, marker='x', color='red')

        plt.show()

    return dbi_, di_

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('-m', '--multiple', type=int, default=2)
    parser.add_argument('-r', '--repeat', type=int, default=1)
    parser.add_argument('datafile')
    args = parser.parse_args()

    seeds = [43, 178, 13]

    dbis = []
    dis = []
    for seed in seeds:
        random.seed(seed)
        dbi_, di_ = kmeans(args)
        dbis.append(dbi_)
        dis.append(di_)

    print 'dbi:', dbis, 'mean = {}'.format(sum(dbis) / len(dbis))
    print 'dis:', dis, 'mean = {}'.format(sum(dis) / len(dis))

