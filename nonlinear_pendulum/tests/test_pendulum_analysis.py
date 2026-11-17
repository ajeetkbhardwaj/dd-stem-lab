import pytest
import numpy as np
from src.pendulum_dynamics import NonlinearPendulum
from src.equilibrium_analysis import calculate_jacobian, analyze_equilibria

def test_equilibria():
    pendulum = NonlinearPendulum(b=0.0)
    eqs = analyze_equilibria(pendulum)
    theta_stars = [eq["theta_star"] for eq in eqs]
    assert 0.0 in theta_stars
    assert np.pi in theta_stars

def test_jacobian():
    pendulum = NonlinearPendulum(m=1.0, L=1.0, g=9.81, b=0.0)
    J = calculate_jacobian(pendulum, 0.0)
    assert np.allclose(J, [[0, 1], [-9.81, 0]])

def test_stability_downward():
    pendulum = NonlinearPendulum(b=1.0)
    J = calculate_jacobian(pendulum, 0.0)
    eigvals = np.linalg.eigvals(J)
    assert all(np.real(e) < 0 for e in eigvals)

def test_stability_upright():
    pendulum = NonlinearPendulum(b=1.0)
    J = calculate_jacobian(pendulum, np.pi)
    eigvals = np.linalg.eigvals(J)
    assert any(np.real(e) > 0 for e in eigvals)
