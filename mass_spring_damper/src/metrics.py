import numpy as np

def calculate_rmse(x_method, x_ref):
    return np.sqrt(np.mean((x_method - x_ref)**2))

def calculate_mae(x_method, x_ref):
    return np.mean(np.abs(x_method - x_ref))
