#!/usr/bin/env python3

# encoding: utf-8
import sys
import math
import csv
from collections import namedtuple, Counter
import numpy as np
import pprint

pprinter = pprint.PrettyPrinter()

laplace = True

features = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感', '密度', '含糖率', '好瓜']
Sample = namedtuple('Sample', features)

def count(samples, predicate):
    count = 0
    for sample in samples:
        if predicate(sample):
            count += 1
    return count

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename, 'r')
    reader = csv.reader(file)
    D = []
    for row in reader:
        row[6] = float(row[6])
        row[7] = float(row[7])
        D.append(Sample._make(row))
    N = len(D)

    P_c = {}
    P_x_c = {}

    for 好瓜 in ('是', '否'):
        Dc = list(filter(lambda x: x.好瓜 == 好瓜, D))
        p = (len(Dc) + 1) / (len(D) + 2) if laplace \
                else len(Dc) / len(D)
        P_c[好瓜] = p
        P_x_c[好瓜] = {}
        print('P(好瓜={}) = {}/{} = {:.3}'.format(好瓜, len(Dc), len(D), p))

        # 离散属性
        for fi, feature in enumerate(features[:6]):
            # calculate P(feature|class)
            counter = Counter()
            values = (sample[fi] for sample in Dc)
            counter.update(values)
            P_x_c[好瓜][feature] = {}
            for value in counter:
                count = counter[value]
                count_ = count + 1 if laplace else count
                len_Dc_ = len(Dc) + len(counter) if laplace \
                        else len(Dc)
                P_xi_c = count_ / len_Dc_
                print('P({}={} | 好瓜={}) = {}/{} = {:.3}'.format(
                    feature, value, 好瓜, 
                    count_, len_Dc_, P_xi_c))
                P_x_c[好瓜][feature][value] = P_xi_c

        # 连续属性
        for fi in range(6, 8):
            feature = features[fi]
            # calculate P(feature|class)
            values = [sample[fi] for sample in Dc]
            mu = np.mean(values)
            sigma = np.std(values, ddof=1)
            print('({},好瓜={}): mu = {:.3}, sigma = {:.3}'.format(
                feature, 好瓜, mu, sigma))
            P_x_c[好瓜][feature] = (mu, sigma)

#    pprinter.pprint(P_c)
#    pprinter.pprint(P_x_c)

    # testing
    x = Sample(色泽='青绿', 根蒂='蜷缩', 敲声='浊响', 纹理='清晰',
            脐部='凹陷', 触感='硬滑', 密度=0.697, 含糖率=0.460,
            好瓜=None)


    for 好瓜 in ('是', '否'):
        product = P_c[好瓜]
        for fi, feature in enumerate(features[:6]):
            xi = x[fi]
            P_xi_c = P_x_c[好瓜][feature][xi]
            print('P({}={} | 好瓜={}) = {:.3}'.format(
                feature, xi, 好瓜, P_xi_c))
            product *= P_xi_c

        for fi in range(6, 8):
            feature = features[fi]
            mu, sigma = P_x_c[好瓜][feature]
            xi = x[fi]
            P_xi_c = 1 / (math.sqrt(2 * math.pi) * sigma) \
                    * math.exp(-(xi - mu) ** 2 / (2 * sigma ** 2))
            print('P({}={} | 好瓜={}) = {:.3}'.format(
                feature, xi, 好瓜, P_xi_c))
            product *= P_xi_c

        print('好瓜={}: {}'.format(好瓜, product))

