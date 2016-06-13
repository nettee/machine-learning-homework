#!/usr/bin/env python

import sys
import numpy as np
from matplotlib import pyplot as plt

import tenfold
import leaveone
import lda

def train(train_set):
    pos_train_set, neg_train_set = train_set

    pos_train_mat = lda.data2mat(pos_train_set)
    neg_train_mat = lda.data2mat(neg_train_set)

#    lda.plot_data(pos_train_mat, neg_train_mat)
#    plt.show()

    w, project_points = lda.lda(pos_train_mat, neg_train_mat)
#    print 'w = ', w
#    print 'project_points =', project_points
    return (w, project_points)

def test(test_set, w, project_points):
    pos_value, neg_value = project_points

    pos_test_set, neg_test_set = test_set
    yes_cnt = 0
    no_cnt = 0
    for x in pos_test_set:
        value = sum(x * y for (x, y) in zip(w, x))
        if abs(value - pos_value) <= abs(value - neg_value):
            yes_cnt += 1
        else:
            no_cnt += 1

    for x in neg_test_set:
        value = sum(x * y for (x, y) in zip(w, x))
        if abs(value - neg_value) <= abs(value - pos_value):
            yes_cnt += 1
        else:
            no_cnt += 1

    error_ratio = no_cnt * 1.0 / (yes_cnt + no_cnt)

    return error_ratio

if __name__ == '__main__':

    filename = sys.argv[1]

    pos_data, neg_data = lda.read_data_raw(filename)
#    print len(pos_data), len(neg_data)

    tenfold_list = tenfold.tenfold_list([pos_data, neg_data])
    #tenfold_list = leaveone.leaveone_list([pos_data, neg_data])

    error_ratio_list = []
    for test_set, train_set in tenfold_list:
#        print len(test_set[0]), len(test_set[1]),
#        print len(train_set[0]), len(train_set[1])

        w, project_points = train(train_set)
        error_ratio = test(test_set, w, project_points)
        error_ratio_list.append(error_ratio)

    erl = np.array(error_ratio_list)
    mean = np.mean(erl)
    stdvar = np.std(erl)
    print 'mean =', mean
    print 'stdvar =', stdvar
