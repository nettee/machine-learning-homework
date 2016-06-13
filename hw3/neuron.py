#!/usr/bin/env python

import math
import random
import numpy as np

class Perceptron:

    def __init__(self, n, eta=0.1):
        self.n = n

        # fixed params
        self.f = lambda x : 1 if x >= 0 else 0
        self.eta = eta

        # params
        self.ws = [random.random() for _ in range(n)]
        self.theta = random.random()
#        self.ws = [1 for _ in range(n)]
#        self.theta = 1

    def print_params(self):
        print self.ws, self.theta

    def work(self, *xs):
        in_ = sum(x * w for (x, w) in zip(xs, self.ws)) - self.theta
        out = self.f(in_)
        return out

    def learn(self, xs, expected):
        self.last_ws = self.ws
        self.last_theta = self.theta

        out = self.work(*xs)
        step = self.eta * (expected - out)
        self.ws = [w + step * x
                for (w, x) in zip(self.ws, xs)]
        self.theta = self.theta - step
        return expected != out

    @property
    def distance(self):
        return math.sqrt(
                sum((w0 - w) ** 2 
                    for (w0, w) in zip(self.last_ws, self.ws)) 
                + (self.last_theta - self.theta) ** 2)

    def test(self, xs):
        return self.work(*xs) == 1


if __name__ == '__main__':

    pc = Perceptron(2)
    print pc.f(0.1)
    print pc.f(0)
    print pc.f(-0.1)

    print pc.work(0.3, 0.4)
    pc.print_params()

    while True:
        changed = pc.learn([0.3, 0.4], 1)
        pc.print_params()
        if not changed:
            break
