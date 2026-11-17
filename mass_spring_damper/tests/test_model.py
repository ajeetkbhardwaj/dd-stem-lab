import pytest
import numpy as np
from src.state_space import StateSpaceModel
from src.transfer_function import calculate_tf_parameters
from src.integrators import rk4, explicit_euler

def test_eigenvalues_match_poles():
    m, c, k = 2.0, 4.0, 20.0
    model = StateSpaceModel(m, c, k)
    tf = calculate_tf_parameters(m, c, k)
    eigvals = np.linalg.eigvals(model.A)
    assert np.allclose(np.sort(eigvals), np.sort(tf["poles"]))

def test_final_position():
    m, c, k = 2.0, 4.0, 20.0
    model = StateSpaceModel(m, c, k)
    t, x = rk4(model, (0, 10), [0.0, 0.0], 0.01)
    assert np.isclose(x[-1, 0], 0.5, atol=1e-2)

def test_damping_type():
    tf = calculate_tf_parameters(2.0, 4.0, 20.0)
    assert tf["damping_type"] == "underdamped"
