import numpy as np

class NonlinearPendulum:
    def __init__(self, m=1.0, L=1.0, g=9.81, b=0.0):
        self.m = m
        self.L = L
        self.g = g
        self.b = b

    def rhs(self, t, state, tau=0.0):
        theta, omega = state
        theta_dot = omega
        omega_dot = - (self.g / self.L) * np.sin(theta) - (self.b / (self.m * self.L**2)) * omega + tau / (self.m * self.L**2)
        return np.array([theta_dot, omega_dot])

class LinearPendulum:
    def __init__(self, m=1.0, L=1.0, g=9.81, b=0.0):
        self.m = m
        self.L = L
        self.g = g
        self.b = b

    def rhs(self, t, state, tau=0.0):
        theta, omega = state
        theta_dot = omega
        omega_dot = - (self.g / self.L) * theta - (self.b / (self.m * self.L**2)) * omega + tau / (self.m * self.L**2)
        return np.array([theta_dot, omega_dot])
