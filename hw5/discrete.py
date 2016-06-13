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
        return [item.strip("'") for item in row]
    return [santinize(row) for row in reader]

class NaiveBayes:

    trained = False

    def __init__(self, D):
        self.classes = set(x[-1] for x in D)
        self.N_feature = len(D[0]) - 1
        self.Ns = [len(set(x[i] for x in D)) 
            for i in range(self.N_feature)]
        print('self.Ns =', self.Ns)

    def train(self, D):

        P_c = {}
        P_x_c = {}

        for cls in self.classes:
            Dc = list(filter(lambda x: x[-1] == cls, D))
            print('class {} has {} items'.format(cls, len(Dc)))

            P_c[cls] = (len(Dc) + 1) / (len(D) + len(self.classes))
            P_x_c[cls] = {}

            for i in range(self.N_feature):
                print('feature[{}] = {}'.format(i, Dc[0][i]))

                counter = Counter()
                values = (x[i] for x in Dc)
                counter.update(values)

                P_x_c[cls][i] = {}
                len_Dc_ = len(Dc) + self.Ns[i]
                P_x_c[cls][i]['_default'] = 1 / len_Dc_
                print('P(x[{}]=_default | {}) = 1/{} = {:.3}'.format(i, cls, len_Dc_, 1 / len_Dc_))
                for value in counter:
                    count = counter[value]
                    count_ = count + 1
                    P_xi_c = count_ / len_Dc_
                    print('P(x[{}]={} | {}) = {}/{} = {:.3}'.format(
                        i, value, cls, count_, len_Dc_, P_xi_c))
                    P_x_c[cls][i][value] = P_xi_c

        self.P_c = P_c
        self.P_x_c = P_x_c

        self.trained = True

    def _cls_likelihood(self, x, cls):
        #print('testing class {}'.format(cls))
        product = self.P_c[cls]
        for i in range(self.N_feature):
            value = x[i]
            if value in self.P_x_c[cls][i]:
                P_xi_c = self.P_x_c[cls][i][value]
            else:
                P_xi_c = self.P_x_c[cls][i]['_default']
            #print('P(x[{}]={} | {}) = {:.3}'.format( i, value, cls, P_xi_c))
            product *= P_xi_c

        #print('likelihood = {}'.format(product))
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
            bayes = NaiveBayes(D)
            bayes.train(others)
            ratio = bayes.test(one)
            ratios.append(ratio)

    print(len(ratios))
    print('average_correct_ratio =', np.mean(ratios))

    
