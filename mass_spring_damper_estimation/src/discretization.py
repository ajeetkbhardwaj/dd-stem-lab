import numpy as np
from scipy.linalg import expm

def discretize_system(A, B, Ts=0.01):
    n = A.shape[0]
    m = B.shape[1]
    
    # Form block matrix [[A, B], [0, 0]]
    block = np.zeros((n + m, n + m))
    block[:n, :n] = A
    block[:n, n:] = B
    
    # Exponentiate
    exp_block = expm(block * Ts)
    
    Ad = exp_block[:n, :n]
    Bd = exp_block[:n, n:]
    return Ad, Bd
