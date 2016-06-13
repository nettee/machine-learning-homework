import numpy as np

def error_ratio(func, pos_mat, neg_mat):
    '''
    func should be a function that returns bool,
    True for positive, false for negative
    '''
    
    yes_cnt = 0
    no_cnt = 0

    for x in pos_mat.T:
        xs = list(x)
        if func(xs) is True:
            yes_cnt += 1
        else:
            no_cnt += 1

    for x in neg_mat.T:
        xs = list(x)
        if func(xs) is False:
            yes_cnt += 1
        else:
            no_cnt += 1

    ratio = no_cnt * 1.0 / (yes_cnt + no_cnt)
    return ratio

