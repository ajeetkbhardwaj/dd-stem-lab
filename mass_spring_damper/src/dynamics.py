import numpy as np

def analytical_step_response(t, m, c, k, u0=10.0):
    x_ss = u0 / k
    omega_n = np.sqrt(k / m)
    zeta = c / (2 * np.sqrt(m * k))
    
    if zeta < 1.0:
        omega_d = omega_n * np.sqrt(1 - zeta**2)
        phi = np.arctan2(np.sqrt(1 - zeta**2), zeta)
        x = x_ss * (1 - np.exp(-zeta * omega_n * t) / np.sqrt(1 - zeta**2) * np.sin(omega_d * t + phi))
    elif np.isclose(zeta, 1.0):
        x = x_ss * (1 - (1 + omega_n * t) * np.exp(-omega_n * t))
    else:
        s1 = -zeta * omega_n + omega_n * np.sqrt(zeta**2 - 1)
        s2 = -zeta * omega_n - omega_n * np.sqrt(zeta**2 - 1)
        x = x_ss * (1 - (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s2 - s1))
    return x

def calculate_energy(x, v, m, k):
    return 0.5 * m * v**2 + 0.5 * k * x**2
