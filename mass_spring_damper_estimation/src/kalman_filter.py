import numpy as np

class KalmanFilter:
    def __init__(self, Ad, Bd, C, Q, R, x0, P0):
        self.Ad = Ad
        self.Bd = Bd
        self.C = C
        self.Q = Q
        self.R = R
        
        self.x_est = np.asarray(x0).flatten()
        self.P = P0.copy()
        
        self.K_history = []
        self.P_trace_history = []
        
    def predict(self, u):
        u = np.asarray(u).flatten()
        self.x_est = (self.Ad @ self.x_est) + (self.Bd @ u).flatten()
        self.P = self.Ad @ self.P @ self.Ad.T + self.Q
        return self.x_est
        
    def update(self, y):
        y = np.atleast_1d(y)
        # K = P * C^T * (C * P * C^T + R)^-1
        S = self.C @ self.P @ self.C.T + self.R
        K = self.P @ self.C.T @ np.linalg.inv(S)
        
        # x = x + K * (y - C * x)
        innovation = y - self.C @ self.x_est
        self.x_est = self.x_est + (K @ innovation).flatten()
        
        # P = (I - K * C) * P
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.C) @ self.P
        
        self.K_history.append(K)
        self.P_trace_history.append(np.trace(self.P))
        return self.x_est
