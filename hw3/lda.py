import math
import numpy as np
from matplotlib import pyplot as plt

def data2mat(data):
    mat = np.array(data)
    mat = np.transpose(mat)
    return mat

def read_data_raw(filename):

    file = open(filename, 'r')

    pos_data = []
    neg_data = []
    for line in file:
        line = line.rstrip('\n')
        fields = [field.strip() for field in line.split(',')]
        tag = fields.pop()
        fields = [float(f) for f in fields]
        tag = int(tag)
        if (tag == 1):
            pos_data.append(fields)
        else:
            neg_data.append(fields)

    file.close()

    return (pos_data, neg_data)

def read_data(filename):

    pos_data, neg_data = read_data_raw(filename)

    pos_mat = data2mat(pos_data)
    neg_mat = data2mat(neg_data)

    return (pos_mat, neg_mat)

def plot_data(pos_mat, neg_mat):

    for x in pos_mat.T:
        x = list(x)
        plt.scatter(x[0], x[1], color='red', marker='s')

    for x in neg_mat.T:
        x = list(x)
        plt.scatter(x[0], x[1], color='green', marker='o')


def miu(X):
    # calculate mean of X's columns
    mean = np.mean(X, axis=1)
    return mean

def Sigma(X, miu):
    ''' within-class scatter matrix '''
    d = np.size(X, axis=0)
    Sigma_sum = np.zeros((d, d))
    for xt in X.transpose():
        x = xt.reshape(d, 1)
        miu = miu.reshape(d, 1)
        Sigma_i = np.dot((x - miu), (x - miu).T)
        Sigma_sum += Sigma_i
    return Sigma_sum

def lda(X_0, X_1):
    ''' linear discriminant analysis
    X_0: negative data matrix, of size(d, _)
    X_1: positive data matrix, of size(d, _)
    X_0 and X_1 must have same number of rows

    return: (w, project_points)
    '''
    d = np.size(X_0, axis=0)
    miu_0 = miu(X_0).reshape(d, 1)
    miu_1 = miu(X_1).reshape(d, 1)
    S_w = Sigma(X_0, miu_0) + Sigma(X_1, miu_1)
#    S_b = np.dot((miu_0 - miu_1), (miu_0 - miu_1).T)
#    print 'S_w = ', S_w

    S_w_inv = np.linalg.inv(S_w)
#    print 'S_w_inv = ', S_w_inv

    w = np.dot(S_w_inv, (miu_0 - miu_1))
    w = list((w.T)[0])
    norm = math.sqrt(sum(wx ** 2 for wx in w))
    normed_w = [wx / norm for wx in w]
    w = normed_w

    miu_0 = list(miu_0.reshape(1, d)[0])
    miu_1 = list(miu_1.reshape(1, d)[0])
#    print 'miu_0 = ', miu_0
#    print 'miu_1 = ', miu_1

    w_dot_miu_0 = sum(x * y for (x, y) in zip(w, miu_0))
    w_dot_miu_1 = sum(x * y for (x, y) in zip(w, miu_1))
#    print w_dot_miu_0, w_dot_miu_1

    return (w, (w_dot_miu_0, w_dot_miu_1))

