import numpy as np

def generate_measurements(t_truth, theta_truth, Ts, sigma_theta=0.01):
    """
    Generate digital measurements from a continuous truth trajectory.
    """
    t_k = np.arange(t_truth[0], t_truth[-1] + Ts/2, Ts)
    theta_k_true = np.interp(t_k, t_truth, theta_truth)
    noise = np.random.normal(0, sigma_theta, size=len(t_k))
    theta_k = theta_k_true + noise
    return t_k, theta_k, theta_k_true

def reconstruct_velocity(t_k, theta_k):
    """
    Estimate velocity using forward finite difference.
    Returns array of same length as t_k, padding last element.
    """
    Ts = t_k[1] - t_k[0] if len(t_k) > 1 else 1.0
    omega_k = np.zeros_like(theta_k)
    if len(theta_k) > 1:
        omega_k[:-1] = (theta_k[1:] - theta_k[:-1]) / Ts
        omega_k[-1] = omega_k[:-2][-1]  # Simple padding
    return omega_k
