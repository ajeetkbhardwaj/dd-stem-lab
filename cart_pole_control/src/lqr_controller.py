import numpy as np
from scipy.linalg import solve_continuous_are

def lqr(A, B, Q, R):
    """Solve continuous-time LQR: returns gain K and Riccati solution P."""
    P = solve_continuous_are(A, B, Q, R)
    K = np.linalg.inv(R) @ B.T @ P
    return K, P

LQR_CONFIGS = {
    "Conservative": {
        "Q": np.diag([1, 0.1, 10, 0.1]),
        "R": np.array([[10.0]])
    },
    "Baseline": {
        "Q": np.diag([10, 1, 100, 1]),
        "R": np.array([[1.0]])
    },
    "Aggressive": {
        "Q": np.diag([100, 10, 1000, 10]),
        "R": np.array([[0.1]])
    },
}
