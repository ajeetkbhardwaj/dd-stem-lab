import pytest
import numpy as np
from src.dynamics import get_continuous_system, check_observability
from src.discretization import discretize_system

def test_observability():
    A, B, C = get_continuous_system()
    is_obs, O = check_observability(A, C)
    assert is_obs, "System should be fully observable"

def test_discretization_identity():
    A, B, C = get_continuous_system()
    Ad, Bd = discretize_system(A, B, Ts=0.01)
    # Ad should approximate I + A*Ts for small Ts (first-order Taylor; use loose tolerance)
    approx = np.eye(2) + A * 0.01
    assert np.allclose(Ad, approx, atol=5e-3)

def test_Ad_stability():
    A, B, C = get_continuous_system()
    Ad, Bd = discretize_system(A, B, Ts=0.01)
    eigvals = np.linalg.eigvals(Ad)
    # For a stable system all discrete eigenvalues should be inside unit circle
    assert np.all(np.abs(eigvals) < 1.0), "Discrete system should be stable"
