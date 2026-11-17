"""
pendulum.py — PendulumSimulator class.

Models a simple pendulum with viscous damping and optional external torque.
Provides RHS computation and wrappers around multiple integration methods.
"""

import numpy as np
from scipy.integrate import solve_ivp


class PendulumSimulator:
    """Simulate a damped simple pendulum.

    Equation of motion (nonlinear):

        m L² θ̈ + b θ̇ + m g L sin(θ) = τ(t)

    State vector:  x = [θ, θ̇]
    """

    def __init__(self, m: float = 1.0, L: float = 1.0,
                 g: float = 9.81, b: float = 0.1):
        self.m = m
        self.L = L
        self.g = g
        self.b = b

    # ------------------------------------------------------------------ #
    #  Derived quantities (small-angle / linearised)
    # ------------------------------------------------------------------ #
    @property
    def omega_0(self) -> float:
        """Undamped natural frequency ω₀ = √(g/L)."""
        return np.sqrt(self.g / self.L)

    @property
    def omega_n(self) -> float:
        """Natural frequency used in damping-ratio definition (same as ω₀)."""
        return self.omega_0

    @property
    def zeta(self) -> float:
        """Damping ratio ζ = b / (2 m L² ωₙ)."""
        return self.b / (2.0 * self.m * self.L ** 2 * self.omega_n)

    @property
    def omega_d(self) -> float:
        """Damped natural frequency ωd = ωₙ √(1 − ζ²).  Valid only if ζ < 1."""
        if self.zeta >= 1.0:
            raise ValueError("System is critically/over-damped; ωd is not real.")
        return self.omega_n * np.sqrt(1.0 - self.zeta ** 2)

    # ------------------------------------------------------------------ #
    #  Right-hand side
    # ------------------------------------------------------------------ #
    def rhs(self, t: float, state: np.ndarray,
            torque=None) -> np.ndarray:
        """Compute dx/dt for the pendulum ODE.

        Parameters
        ----------
        t : float   — current time
        state : array [θ, θ̇]
        torque : callable(t) → float, or None (defaults to 0)

        Returns
        -------
        dstate : array [θ̇, θ̈]
        """
        theta, theta_dot = state
        tau = torque(t) if torque is not None else 0.0
        mL2 = self.m * self.L ** 2
        theta_ddot = (
            -self.g / self.L * np.sin(theta)
            - self.b / mL2 * theta_dot
            + tau / mL2
        )
        return np.array([theta_dot, theta_ddot])

    # ------------------------------------------------------------------ #
    #  Simulation drivers
    # ------------------------------------------------------------------ #
    def simulate(self, t_span, initial_state, torque=None,
                 method="DOP853", max_step=np.inf,
                 dt=None, t_eval=None,
                 rtol=1e-12, atol=1e-14):
        """Run a simulation and return (t, states).

        Parameters
        ----------
        t_span : (t0, tf)
        initial_state : [θ₀, θ̇₀]
        torque : callable(t) → float, or None
        method : str — one of 'euler', 'rk4', 'RK45', 'DOP853'
        max_step : float — max step for adaptive solvers
        dt : float — fixed step size for 'euler' / 'rk4'
        t_eval : array — times at which to report the solution
        rtol, atol : float — tolerances for adaptive solvers

        Returns
        -------
        t : 1-D array of time values
        y : 2-D array of shape (len(t), 2)  — columns [θ, θ̇]
        """
        y0 = np.asarray(initial_state, dtype=float)

        if method.lower() == "euler":
            return self._euler(t_span, y0, torque, dt)
        elif method.lower() == "rk4":
            return self._rk4(t_span, y0, torque, dt)
        else:
            return self._scipy_solve(t_span, y0, torque,
                                     method=method, max_step=max_step,
                                     t_eval=t_eval,
                                     rtol=rtol, atol=atol)

    # ---------- fixed-step Euler ---------- #
    def _euler(self, t_span, y0, torque, dt):
        if dt is None:
            raise ValueError("dt must be provided for Euler method.")
        t0, tf = t_span
        t_arr = np.arange(t0, tf + dt * 0.5, dt)
        y = np.zeros((len(t_arr), 2))
        y[0] = y0
        for i in range(len(t_arr) - 1):
            y[i + 1] = y[i] + dt * self.rhs(t_arr[i], y[i], torque)
        return t_arr, y

    # ---------- fixed-step classical RK4 ---------- #
    def _rk4(self, t_span, y0, torque, dt):
        if dt is None:
            raise ValueError("dt must be provided for RK4 method.")
        t0, tf = t_span
        t_arr = np.arange(t0, tf + dt * 0.5, dt)
        y = np.zeros((len(t_arr), 2))
        y[0] = y0
        for i in range(len(t_arr) - 1):
            ti = t_arr[i]
            yi = y[i]
            k1 = self.rhs(ti, yi, torque)
            k2 = self.rhs(ti + dt / 2, yi + dt / 2 * k1, torque)
            k3 = self.rhs(ti + dt / 2, yi + dt / 2 * k2, torque)
            k4 = self.rhs(ti + dt, yi + dt * k3, torque)
            y[i + 1] = yi + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return t_arr, y

    # ---------- scipy adaptive solvers ---------- #
    def _scipy_solve(self, t_span, y0, torque, method,
                     max_step, t_eval, rtol, atol):
        def f(t, y):
            return self.rhs(t, y, torque)

        sol = solve_ivp(f, t_span, y0, method=method,
                        max_step=max_step, t_eval=t_eval,
                        rtol=rtol, atol=atol, dense_output=True)
        if not sol.success:
            raise RuntimeError(f"solve_ivp failed: {sol.message}")
        return sol.t, sol.y.T   # shape (N, 2)

    # ------------------------------------------------------------------ #
    #  Energy
    # ------------------------------------------------------------------ #
    def energy(self, state: np.ndarray) -> np.ndarray:
        """Total mechanical energy E = ½ m L² θ̇² + m g L (1 − cos θ).

        Parameters
        ----------
        state : array of shape (N, 2) or (2,)

        Returns
        -------
        E : scalar or 1-D array
        """
        state = np.atleast_2d(state)
        theta = state[:, 0]
        theta_dot = state[:, 1]
        KE = 0.5 * self.m * self.L ** 2 * theta_dot ** 2
        PE = self.m * self.g * self.L * (1.0 - np.cos(theta))
        return (KE + PE).squeeze()
