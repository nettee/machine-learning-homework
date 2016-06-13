#!/usr/bin/env python

import sys
import numpy as np
from matplotlib import pyplot as plt

import lda

if __name__ == '__main__':

    filename = sys.argv[1]

    pos_mat, neg_mat = lda.read_data(filename)

    lda.plot_data(pos_mat, neg_mat)

    print pos_mat
    print neg_mat

    w, project_points = lda.lda(neg_mat, pos_mat)

    if w[1] < 0:
        w = [-x for x in w]
    print 'w = ', w
    print 'project_points = ', project_points

    # draw vector w
    plt.plot(*zip((0, 0), w), color='blue')

    plt.axis([0, 1, 0, 1])

    plt.show()
