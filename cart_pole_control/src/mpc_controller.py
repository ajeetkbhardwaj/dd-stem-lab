import numpy as np
from scipy.linalg import expm

class MPCController:
    """Linear MPC via quadratic programming (closed-form for unconstrained,
    with input saturation clip applied after solving)."""
    def __init__(self, Ad, Bd, Q, R, H=20, u_max=20.0, x_max=None, theta_max=0.35):
        self.Ad    = Ad
        self.Bd    = Bd
        self.Q     = Q
        self.R     = R
        self.H     = H
        self.u_max = u_max
        self.theta_max = theta_max

        # Pre-build prediction matrices
        n  = Ad.shape[0]
        m  = Bd.shape[1]
        Phi = np.zeros((n * H, n))
        Gamma = np.zeros((n * H, m * H))

        Ak = np.eye(n)
        for i in range(H):
            Ak = Ad @ Ak
            Phi[i*n:(i+1)*n, :] = Ak
            for j in range(i + 1):
                Gamma[i*n:(i+1)*n, j*m:(j+1)*m] = (
                    np.linalg.matrix_power(Ad, i - j) @ Bd
                )

        Q_bar = np.kron(np.eye(H), Q)
        R_bar = np.kron(np.eye(H), R)

        self.H_qp  = Gamma.T @ Q_bar @ Gamma + R_bar
        self.F_qp  = Gamma.T @ Q_bar @ Phi

    def compute(self, x):
        x = np.asarray(x).flatten()
        f  = self.F_qp @ x
        U_opt = -np.linalg.solve(self.H_qp, f)
        u0 = float(np.clip(U_opt[0], -self.u_max, self.u_max))
        return u0


def discretize(A, B, Ts):
    n, m = A.shape[0], B.shape[1]
    block = np.zeros((n + m, n + m))
    block[:n, :n] = A
    block[:n, n:] = B
    exp_block = expm(block * Ts)
    return exp_block[:n, :n], exp_block[:n, n:]
