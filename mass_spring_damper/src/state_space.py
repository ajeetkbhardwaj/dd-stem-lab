import numpy as np

class StateSpaceModel:
    def __init__(self, m, c, k):
        self.m = m
        self.c = c
        self.k = k
        self.A = np.array([
            [0, 1],
            [-k/m, -c/m]
        ])
        self.B = np.array([
            [0],
            [1/m]
        ])
        self.C = np.array([[1, 0]])
        self.D = np.array([[0]])

    def state_derivative(self, x, u):
        return self.A @ x + self.B @ np.array([u])
