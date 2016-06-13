#!/usr/bin/env python

import random

F = 10

def tenfold(dataset):

    '''
    dataset: set of data

    return: [(one_1, other_1), (one_2, other_2) 
            ..., (one_F, other_F)]
    '''

    N = len(dataset)
    random.shuffle(dataset)

    # split dataset evenly into F parts
    splits = [int(round(i * N * 1.0 / F)) for i in range(F)]
    dataset_collection = []
    for i in range(len(splits)):
        if i < len(splits) - 1:
            s = splits[i]
            sa = splits[i+1]
            dataset_collection.append(dataset[s:sa])
        else:
            s = splits[i]
            dataset_collection.append(dataset[s:])

    tenfold_collection = []
    for i in range(len(dataset_collection)):
        one = dataset_collection[i]
        other = []
        for j in range(len(dataset_collection)):
            if j != i:
                other += dataset_collection[j]
        tenfold_collection.append((one, other))

    return tenfold_collection

def tenfold_list(dataset_list):
    '''
    dataset_list: list of [(one_1, other_1),
            (one_2, other_2),
            ...
            (one_F, other_F)]

    return: [[list of one_1, list of other_1],
            [list of one_2, list of other_2],
            ...
            [list of one_F, list of other_F]]
    '''
    temp = zip(*[tenfold(dataset) for dataset in dataset_list])
    return [zip(*item) for item in temp]

if __name__ == '__main__':
    dataset_collection = tenfold(range(35))
    #print dataset_collection

    c = tenfold_list([range(1, 11), range(-1, -11, -1)])
    for item in c:
        print item
    
