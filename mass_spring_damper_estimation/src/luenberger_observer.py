import numpy as np
from scipy.signal import place_poles

class LuenbergerObserver:
    def __init__(self, A, B, C, L, x0):
        self.A = A
        self.B = B
        self.C = C
        self.L = L
        self.x_est = x0.copy()
        
    def update(self, y, u, Ts=0.01):
        # Continuous-time observer: dx_hat/dt = A*x_hat + B*u + L*(y - C*x_hat)
        # Discrete approximation via Euler integration
        y = np.asarray(y).flatten()
        u = np.asarray(u).flatten()
        y_hat = (self.C @ self.x_est).flatten()
        innovation = y - y_hat
        dx = (self.A @ self.x_est).flatten() + (self.B @ u).flatten() + (self.L @ innovation).flatten()
        self.x_est = self.x_est + Ts * dx
        return self.x_est.copy()


def design_observer_gain(A, C, desired_poles=(-20+20j, -20-20j)):
    result = place_poles(A, C.T, desired_poles)
    L = result.gain_matrix.T
    return L
