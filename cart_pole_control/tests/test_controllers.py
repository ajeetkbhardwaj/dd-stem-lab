import pytest
import numpy as np
from src.cart_pole_dynamics import nonlinear_dynamics, get_linearized_system, check_controllability
from src.lqr_controller import lqr, LQR_CONFIGS
from src.simulation import simulate

def test_controllability():
    A, B, C = get_linearized_system()
    rank, _ = check_controllability(A, B)
    assert rank == 4, "Cart-pole must be fully controllable"

def test_open_loop_unstable():
    A, B, C = get_linearized_system()
    eigvals = np.linalg.eigvals(A)
    assert any(np.real(e) > 0 for e in eigvals), "Open-loop must be unstable"

def test_lqr_stable():
    A, B, C = get_linearized_system()
    K, _ = lqr(A, B, LQR_CONFIGS["Baseline"]["Q"], LQR_CONFIGS["Baseline"]["R"])
    cl_eigs = np.linalg.eigvals(A - B @ K)
    assert all(np.real(e) < 0 for e in cl_eigs), "LQR closed-loop must be stable"

def test_nonlinear_dynamics():
    state = np.zeros(4)
    # At rest, no force -> zero acceleration
    xdot = nonlinear_dynamics(state, 0.0)
    assert np.allclose(xdot, 0.0, atol=1e-10)

def test_saturation():
    from src.cart_pole_dynamics import nonlinear_dynamics
    # Apply huge force; clip should keep xdd finite
    state = np.array([0, 0, 0.01, 0])
    xdot_clipped = nonlinear_dynamics(state, 1e6)
    xdot_max     = nonlinear_dynamics(state, 20.0)
    assert np.allclose(xdot_clipped, xdot_max, atol=1e-8)
