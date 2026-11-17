import numpy as np

def calculate_tf_parameters(m, c, k):
    omega_n = np.sqrt(k / m)
    zeta = c / (2 * np.sqrt(m * k))
    
    if zeta == 0:
        damping_type = "undamped"
    elif zeta < 1:
        damping_type = "underdamped"
    elif np.isclose(zeta, 1.0):
        damping_type = "critically damped"
    else:
        damping_type = "overdamped"
        
    poles = np.roots([m, c, k])
    stable = all(np.real(p) < 0 for p in poles) if zeta > 0 else "marginally stable"
    
    return {
        "omega_n": omega_n,
        "omega_d": omega_n * np.sqrt(1 - zeta**2) if zeta < 1 else None,
        "zeta": zeta,
        "damping_type": damping_type,
        "poles": poles,
        "stable": stable
    }
