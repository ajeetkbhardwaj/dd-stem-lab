import pytest
import numpy as np
from src.pendulum import PendulumSimulator

def test_omega_0():
    sim = PendulumSimulator(m=1.0, L=1.0, g=9.81, b=0.0)
    assert np.isclose(sim.omega_0, np.sqrt(9.81/1.0))

def test_rhs():
    sim = PendulumSimulator(m=1.0, L=1.0, g=9.81, b=0.1)
    state = [0.0, 0.0]
    deriv = sim.rhs(0.0, state)
    assert np.allclose(deriv, [0.0, 0.0])
