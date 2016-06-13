#!/usr/bin/env python

import sys
import math
from matplotlib import pyplot as plt

import lda
import neuron
import error

eta = 0.3

def distance(last, current):
    last_ws, last_theta = last
    ws, theta = current
    return math.sqrt(
            sum((w0 - w) ** 2 for (w0, w) in zip(last_ws, ws))
            + (last_theta - theta) ** 2)

if __name__ == '__main__':

    filename = sys.argv[1]

    pos_mat, neg_mat = lda.read_data(filename)
    lda.plot_data(pos_mat, neg_mat)

    pc = neuron.Perceptron(2, eta=eta)

    max_round = 5000
    nr_round = 0

    while nr_round < max_round:

        last = (pc.ws, pc.theta)

        for x in pos_mat.T:
            xs = list(x)
            pc.learn(xs, 1)

        for x in neg_mat.T:
            xs = list(x)
            pc.learn(xs, 0)

        current = (pc.ws, pc.theta)
        dist = distance(last, current)
        #print current, dist

        if dist < 1e-4:
            break

        nr_round += 1

    print nr_round, 'rounds in total'

    # specific to ls.csv
    y0 = pc.theta / pc.ws[1]
    y1 = (pc.theta - 5 * pc.ws[0]) / pc.ws[1]
    print y0, y1
    plt.plot(*zip((0, y0), (5, y1)), color='blue')
    plt.axis([0, 5, 0, 5])

    #plt.show()

    error_ratio = error.error_ratio(pc.test, pos_mat, neg_mat)
    print 'error_radio =', error_ratio
