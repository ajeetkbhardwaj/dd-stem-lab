import numpy as np

# System parameters
M  = 1.0    # cart mass (kg)
mp = 0.1    # pole mass (kg)
l  = 0.5    # pole half-length (m)
g  = 9.81   # gravity (m/s^2)

def nonlinear_dynamics(state, force, M=M, mp=mp, l=l, g=g):
    """
    state = [x, x_dot, theta, theta_dot]
    Returns state_dot.
    """
    x, xd, th, thd = state
    u = np.clip(force, -20.0, 20.0)   # actuator saturation

    sin_th = np.sin(th)
    cos_th = np.cos(th)
    denom  = M + mp * sin_th**2

    xdd  = (u + mp * sin_th * (l * thd**2 + g * cos_th)) / denom
    thdd = (-u * cos_th - mp * l * thd**2 * sin_th * cos_th
            - (M + mp) * g * sin_th) / (l * denom)

    return np.array([xd, xdd, thd, thdd])


def get_linearized_system(M=M, mp=mp, l=l, g=g):
    """Linearization around upright equilibrium (0,0,0,0), u*=0."""
    A = np.array([
        [0, 1,                   0, 0],
        [0, 0,         -mp*g/M,   0],
        [0, 0,                   0, 1],
        [0, 0,   (M+mp)*g/(M*l),  0],
    ])
    B = np.array([[0], [1/M], [0], [-1/(M*l)]])
    C = np.eye(4)
    return A, B, C


def check_controllability(A, B):
    n = A.shape[0]
    cols = [B]
    for i in range(1, n):
        cols.append(np.linalg.matrix_power(A, i) @ B)
    Cmat = np.hstack(cols)
    return np.linalg.matrix_rank(Cmat), Cmat
