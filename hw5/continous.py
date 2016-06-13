#!/usr/bin/env python3

# encoding: utf-8
import sys
import math
import csv
from collections import Counter
import numpy as np
import pprint

import tenfold

pprinter = pprint.PrettyPrinter()

def read_data(filename):
    file = open(filename, 'r')
    reader = csv.reader(file)
    def santinize(row):
        row = [item.strip("'") for item in row]
        for i in range(len(row) - 1):
            row[i] = float(row[i])
        return row
    return [santinize(row) for row in reader]

class ContinousNaiveBayes:

    trained = False

    def __init__(self, D):
        self.classes = set(x[-1] for x in D)
        self.N_feature = len(D[0]) - 1
#        self.Ns = [len(set(x[i] for x in D)) 
#            for i in range(self.N_feature)]
#        print('self.Ns =', self.Ns)

    def train(self, D):

        P_c = {}
        P_x_c = {}

        for cls in self.classes:
            Dc = list(filter(lambda x: x[-1] == cls, D))
            print('class "{}" has {} items'.format(cls, len(Dc)))

#            P_c[cls] = (len(Dc) + 1) / (len(D) + len(self.classes))
            P_c[cls] = len(Dc) / len(D)
            P_x_c[cls] = {}

            for i in range(self.N_feature):

                values = [x[i] for x in Dc]

                mu = np.mean(values)
                sigma = np.std(values, ddof=1)
                print('feature[{}], "{}": mu = {:.3}, sigma = {:.3}'.format(i, cls, mu, sigma))
                P_x_c[cls][i] = (mu, sigma)

        pprinter.pprint(P_c)
        pprinter.pprint(P_x_c)

        self.P_c = P_c
        self.P_x_c = P_x_c

        self.trained = True

    def _cls_likelihood(self, x, cls):
#        print('testing class {}'.format(cls))
        product = self.P_c[cls]
        for i in range(self.N_feature):
            mu, sigma = self.P_x_c[cls][i]
            xi = x[i]
            if abs(mu) < 1e-6 and abs(sigma) < 1e-6:
                if abs(xi) < 1e-6:
                    P_xi_c = 1
                else:
                    P_xi_c = 1e-3
            else:
                P_xi_c = 1 / (math.sqrt(2 * math.pi) * sigma) \
                    * math.exp(-(xi - mu) ** 2 / (2 * sigma ** 2))
#            print('P_xi_c =', P_xi_c)
            product *= P_xi_c

#        print('likelihood = {}'.format(product))
        return product

    def _test_sample(self, x):
        print('testing {}'.format(x))
        likelies = {cls : self._cls_likelihood(x, cls)
                for cls in self.classes}
        print('likelies =', likelies)
        choosed = sorted(likelies.items(), 
                key=lambda u: u[1],
                reverse=True
                )[0][0]
        print('choosed class = {}'.format(choosed))
        if choosed == x[-1]:
            print('Yes')
        else:
            print('No')
        return choosed == x[-1]

    def test(self, T):
        if not self.trained:
            print('Error: not trained')
            return

        results = [self._test_sample(x) for x in T]
        correct_ratio = len([r for r in results if r]) \
                / len(results)
        print('results =', results)
        print('correct_ratio =', correct_ratio)
        return correct_ratio

if __name__ == '__main__':

    D = read_data(sys.argv[1])

    tenfolds = tenfold.tenfold_expanded(D)
    print('------------')
    ratios = []
    for _ in range(5):
        for (one, others) in tenfolds:
            print('len(one) = {}, len(others) = {}'.format(
                len(one), len(others)))
            bayes = ContinousNaiveBayes(D)
            bayes.train(others)
            ratio = bayes.test(one)
            ratios.append(ratio)

    print(len(ratios))
    print('average_correct_ratio =', np.mean(ratios))

    
