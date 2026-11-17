import numpy as np

def get_continuous_system(m=2.0, c=4.0, k=20.0):
    A = np.array([
        [0.0, 1.0],
        [-k/m, -c/m]
    ])
    B = np.array([
        [0.0],
        [1.0/m]
    ])
    C = np.array([[1.0, 0.0]])
    return A, B, C

def check_observability(A, C):
    O = np.vstack((C, C @ A))
    return np.linalg.matrix_rank(O) == A.shape[0], O
