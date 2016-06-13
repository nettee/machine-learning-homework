#!/usr/bin/env python3

import random
import pprint

F = 10

pprinter = pprint.PrettyPrinter(compact=True, width=120)

def seperate_class(D):

    classes = set(x[-1] for x in D)

    S = {cls: [] for cls in classes}
    for i, x in enumerate(D):
        cls = x[-1]
        S[cls].append(i)

    return S

def cut(L, F):
    '''
    split list L evenly info F parts
    '''
    print('cutting {} of length {}'.format(L, len(L)))
    random.shuffle(L)
    splits = [int(round(i * len(L) / F)) for i in range(F)]
    C = []
    for i in range(len(splits)):
        if i < len(splits) - 1:
            s = splits[i]
            sa = splits[i+1]
            C.append(L[s:sa])
        else:
            s = splits[i]
            C.append(L[s:])
    return C

def tenfold(D):

    S = seperate_class(D)

    folds_indexes = [[] for _ in range(F)]
    for indexes in S.values():
        C = cut(indexes, F)
        pprinter.pprint(C)
        for i, c in enumerate(C):
            folds_indexes[i].extend(c)

    folds_indexes = [sorted(indexes) for indexes in folds_indexes]
    pprinter.pprint(folds_indexes)

    folds = [[D[i] for i in indexes] for indexes in folds_indexes]

    return folds

def tenfold_expanded(D):
    folds = tenfold(D)
    folds_expanded = []
    for i, one in enumerate(folds):
        others_indexes = set(range(F)) - set([i])
        print('one = {}, others = {}'.format(i, others_indexes))
        others = []
        for j in others_indexes:
            others.extend(folds[j])
        print('len(one) = {}, len(others) = {}'.format(
            len(one), len(others)))
        
        folds_expanded.append((one, others))

    return folds_expanded
