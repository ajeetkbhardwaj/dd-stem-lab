import numpy as np

def generate_process_noise(Q, num_steps, seed=42):
    np.random.seed(seed)
    # Ensure Q is symmetric positive semi-definite, use multivariate normal
    mean = np.zeros(Q.shape[0])
    return np.random.multivariate_normal(mean, Q, num_steps)

def generate_measurement_noise(R, num_steps, seed=43):
    np.random.seed(seed)
    mean = np.zeros(R.shape[0])
    return np.random.multivariate_normal(mean, R, num_steps)
