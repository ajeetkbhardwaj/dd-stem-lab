import numpy as np
from src.cart_pole_dynamics import nonlinear_dynamics

def simulate(controller_fn, x0, T=5.0, Ts=0.02,
             noise_R=None, disturbance=None, seed=0):
    """
    Simulate the nonlinear cart-pole under controller_fn.

    controller_fn : callable(state) -> scalar force
    noise_R       : 4x4 measurement noise covariance (or None)
    Returns t, states (N,4), forces (N,)
    """
    rng = np.random.default_rng(seed)
    N   = int(T / Ts)
    t   = np.linspace(0, T, N)

    states = np.zeros((N, 4))
    forces = np.zeros(N)

    x = np.asarray(x0, dtype=float).copy()

    for i in range(N):
        # Measurement noise
        if noise_R is not None:
            x_meas = x + rng.multivariate_normal(np.zeros(4), noise_R)
        else:
            x_meas = x.copy()

        u = controller_fn(x_meas)
        u = float(np.clip(u, -20.0, 20.0))

        # External disturbance
        if disturbance is not None:
            u_eff = u + disturbance(t[i])
        else:
            u_eff = u

        states[i] = x
        forces[i] = u

        # RK4 integration
        k1 = nonlinear_dynamics(x, u_eff)
        k2 = nonlinear_dynamics(x + 0.5*Ts*k1, u_eff)
        k3 = nonlinear_dynamics(x + 0.5*Ts*k2, u_eff)
        k4 = nonlinear_dynamics(x + Ts*k3, u_eff)
        x  = x + (Ts/6) * (k1 + 2*k2 + 2*k3 + k4)

        # Detect fall
        if abs(x[2]) > np.pi/2:
            states[i+1:] = x
            forces[i+1:]  = 0.0
            break

    return t, states, forces
