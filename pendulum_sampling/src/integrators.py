"""
integrators.py — Integrator comparison utilities.

Compares fixed-step Euler and RK4 against a high-accuracy DOP853 reference.
Produces convergence data and log-log plots.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.pendulum import PendulumSimulator


def compute_reference(sim: PendulumSimulator, t_span, y0, torque=None):
    """High-accuracy DOP853 reference solution with dense output."""
    from scipy.integrate import solve_ivp

    def f(t, y):
        return sim.rhs(t, y, torque)

    sol = solve_ivp(f, t_span, y0, method="DOP853",
                    rtol=1e-13, atol=1e-15, dense_output=True)
    if not sol.success:
        raise RuntimeError(f"Reference integration failed: {sol.message}")
    return sol


def integrator_convergence_study(sim: PendulumSimulator,
                                 t_span, y0,
                                 step_sizes=None,
                                 torque=None):
    """Run Euler and RK4 at various step sizes and compare to DOP853 reference.

    Returns a DataFrame with columns:
        h, method, rmse_theta, rmse_theta_dot
    """
    if step_sizes is None:
        step_sizes = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]

    ref_sol = compute_reference(sim, t_span, y0, torque)

    rows = []
    for h in step_sizes:
        for method_name in ["euler", "rk4"]:
            t_m, y_m = sim.simulate(t_span, y0, torque=torque,
                                    method=method_name, dt=h)
            # Evaluate reference at the same time points
            y_ref = ref_sol.sol(t_m).T  # shape (N, 2)

            err_theta = y_m[:, 0] - y_ref[:, 0]
            err_omega = y_m[:, 1] - y_ref[:, 1]

            rmse_theta = np.sqrt(np.mean(err_theta ** 2))
            rmse_omega = np.sqrt(np.mean(err_omega ** 2))

            rows.append({
                "h": h,
                "method": method_name.upper(),
                "rmse_theta": rmse_theta,
                "rmse_theta_dot": rmse_omega,
            })

    return pd.DataFrame(rows)


def plot_convergence(df: pd.DataFrame, save_path=None):
    """Log-log convergence plot: RMSE(θ) vs step size h."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for ax, col, label in zip(
            axes,
            ["rmse_theta", "rmse_theta_dot"],
            [r"RMSE $\theta$ [rad]", r"RMSE $\dot{\theta}$ [rad/s]"]):
        for method, grp in df.groupby("method"):
            grp = grp.sort_values("h")
            ax.loglog(grp["h"], grp[col], "o-", label=method)

        # Reference slopes
        h_ref = np.array([df["h"].min(), df["h"].max()])
        y_base = df.loc[df["method"] == "EULER", col].min() * 0.5
        ax.loglog(h_ref, y_base * (h_ref / h_ref[0]) ** 1,
                  "k--", alpha=0.3, label="slope 1")
        ax.loglog(h_ref, y_base * (h_ref / h_ref[0]) ** 4,
                  "k:", alpha=0.3, label="slope 4")

        ax.set_xlabel("Step size  h  [s]")
        ax.set_ylabel(label)
        ax.set_title(f"Convergence: {label}")
        ax.legend()
        ax.grid(True, which="both", ls=":", alpha=0.5)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fig
