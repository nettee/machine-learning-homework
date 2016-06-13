#!/usr/bin/env python

import random

def leaveone(dataset):

    '''
    dataset: set of data

    return [(one_1, other_1),
            (one_2, other_2),
            ...
            (one_N, other_N)]

    '''

    N = len(dataset)

    leaveone_collection = []

    indexes = list(range(N))
    random.shuffle(indexes)

    for index in indexes:
        alldata = list(dataset)
        one = [alldata[index]]
        alldata.pop(index)
        leaveone_collection.append((one, alldata))

    return leaveone_collection

def leaveone_list(dataset_list):
    '''
    '''
    temp = zip(*[leaveone(dataset) for dataset in dataset_list])
    return [zip(*item) for item in temp]

def leaveone_list(dataset_list):

    result = []

    pos_dataset, neg_dataset = dataset_list
    for one, other in leaveone(pos_dataset):
        result.append([(one, []), (other, neg_dataset)])

    for one, other in leaveone(neg_dataset):
        result.append([([], one), (pos_dataset, other)])

    return result

if __name__ == '__main__':
    a = range(9)
    leaveone_collection = leaveone(a)

    c = leaveone_list([range(1, 11), range(-1, -11, -1)])
    for item in c:
        print item

