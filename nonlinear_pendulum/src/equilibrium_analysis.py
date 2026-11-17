import numpy as np

def calculate_jacobian(pendulum, theta_star):
    # J = [[0, 1], [-g/L cos(theta), -b / (mL^2)]]
    g = pendulum.g
    L = pendulum.L
    b = pendulum.b
    m = pendulum.m
    return np.array([
        [0.0, 1.0],
        [- (g / L) * np.cos(theta_star), - b / (m * L**2)]
    ])

def analyze_equilibria(pendulum):
    equilibria = [0.0, np.pi] # Just the primary two in [-pi, pi]
    results = []
    
    for eq in equilibria:
        J = calculate_jacobian(pendulum, eq)
        eigenvalues = np.linalg.eigvals(J)
        stable = all(np.real(e) < 0 for e in eigenvalues) if pendulum.b > 0 else all(np.real(e) <= 0 for e in eigenvalues)
        results.append({
            "theta_star": eq,
            "eigenvalue_1": eigenvalues[0],
            "eigenvalue_2": eigenvalues[1],
            "stable": stable
        })
    return results
