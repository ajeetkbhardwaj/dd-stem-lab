import numpy as np
import pandas as pd
import json

from src.cart_pole_dynamics import (get_linearized_system,
                                     check_controllability, M, mp, l, g)
from src.lqr_controller      import lqr, LQR_CONFIGS
from src.pid_controller      import PIDController
from src.mpc_controller      import MPCController, discretize
from src.simulation          import simulate
from src.metrics             import compute_metrics
from src.plotting            import plot_response, plot_phase, plot_comparison

# ── Constants ─────────────────────────────────────────────────────────────────
Ts   = 0.02
T    = 6.0
x0   = np.array([0.0, 0.0, 0.10, 0.0])   # 0.10 rad initial angle
u_max = 20.0

# Measurement noise (position σ=0.01 m, angle σ=0.02 rad)
R_noise = np.diag([0.0001, 0.0, 0.0004, 0.0])

def main():
    A, B, C = get_linearized_system()
    Ad, Bd  = discretize(A, B, Ts)

    # ── Open-loop check ───────────────────────────────────────────────────────
    eigvals_ol = np.linalg.eigvals(A)
    rank_ctrl, _ = check_controllability(A, B)
    print(f"Open-loop eigenvalues: {eigvals_ol}")
    print(f"System unstable: {any(np.real(e) > 0 for e in eigvals_ol)}")
    print(f"Controllability rank: {rank_ctrl}  (need 4)")

    all_results = {}

    # ══════════════════════════════════════════════════════════════════════════
    # 1. PID
    # ══════════════════════════════════════════════════════════════════════════
    print("\n=== PID ===")
    pid = PIDController(Kp=50, Ki=2, Kd=15, u_max=u_max, Ts=Ts)
    pid.reset()

    def pid_ctrl(state):
        return pid.compute(state[2])

    t, states_pid, forces_pid = simulate(pid_ctrl, x0, T=T, Ts=Ts, seed=0)
    m_pid = compute_metrics(t, states_pid, forces_pid, Ts=Ts)
    all_results["PID"] = m_pid
    print(m_pid)

    plot_response(t, states_pid, forces_pid, "PID Controller",
                  "results/figures/pid_response.png")
    plot_phase(t, states_pid, "PID", "results/figures/pid_phase.png")

    # PID with noise
    pid.reset()
    _, states_pid_noisy, _ = simulate(pid_ctrl, x0, T=T, Ts=Ts,
                                       noise_R=R_noise, seed=7)

    # ══════════════════════════════════════════════════════════════════════════
    # 2. LQR (three tunings)
    # ══════════════════════════════════════════════════════════════════════════
    print("\n=== LQR ===")
    lqr_results = {}
    for name, cfg in LQR_CONFIGS.items():
        K, P = lqr(A, B, cfg["Q"], cfg["R"])
        cl_eigs = np.linalg.eigvals(A - B @ K)
        print(f"  [{name}] closed-loop eigs: {np.round(cl_eigs, 3)}")

        def make_lqr_ctrl(K):
            def ctrl(state):
                return float(np.clip(-K @ state, -u_max, u_max))
            return ctrl

        ctrl = make_lqr_ctrl(K)
        t, states_lqr, forces_lqr = simulate(ctrl, x0, T=T, Ts=Ts, seed=0)
        m = compute_metrics(t, states_lqr, forces_lqr, Ts=Ts)
        lqr_results[name] = m
        all_results[f"LQR_{name}"] = m
        print(f"  [{name}] metrics: {m}")

        plot_response(t, states_lqr, forces_lqr,
                      f"LQR Controller - {name}",
                      f"results/figures/lqr_{name.lower()}_response.png")

    plot_phase(t, states_lqr, "LQR Baseline", "results/figures/lqr_phase.png")

    # ══════════════════════════════════════════════════════════════════════════
    # 3. MPC
    # ══════════════════════════════════════════════════════════════════════════
    print("\n=== MPC ===")
    Q_mpc = np.diag([10, 1, 100, 1])
    R_mpc = np.array([[1.0]])

    for H in [10, 20, 30]:
        mpc = MPCController(Ad, Bd, Q_mpc, R_mpc, H=H, u_max=u_max)

        def make_mpc_ctrl(mpc):
            def ctrl(state):
                return mpc.compute(state)
            return ctrl

        ctrl = make_mpc_ctrl(mpc)
        t, states_mpc, forces_mpc = simulate(ctrl, x0, T=T, Ts=Ts, seed=0)
        m = compute_metrics(t, states_mpc, forces_mpc, Ts=Ts)
        all_results[f"MPC_H{H}"] = m
        print(f"  [H={H}] metrics: {m}")

        plot_response(t, states_mpc, forces_mpc,
                      f"MPC Controller (H={H})",
                      f"results/figures/mpc_H{H}_response.png")

    plot_phase(t, states_mpc, "MPC H=30", "results/figures/mpc_phase.png")

    # ══════════════════════════════════════════════════════════════════════════
    # 4. Comparison plots
    # ══════════════════════════════════════════════════════════════════════════
    compare_set = {
        "PID":        all_results["PID"],
        "LQR_Baseline": all_results["LQR_Baseline"],
        "MPC_H20":    all_results["MPC_H20"],
    }

    plot_comparison(compare_set, "Settling Time (s)", "Time (s)",
                    "Settling Time Comparison", "results/figures/settling_time_cmp.png")
    plot_comparison(compare_set, "RMS force (N)", "Force RMS (N)",
                    "Control Effort Comparison", "results/figures/rms_force_cmp.png")
    plot_comparison(compare_set, "RMSE theta (rad)", "RMSE θ (rad)",
                    "Angle Tracking Error Comparison", "results/figures/rmse_theta_cmp.png")

    # ── Save results ──────────────────────────────────────────────────────────
    df = pd.DataFrame(all_results).T
    df.to_csv("results/controller_comparison.csv")
    with open("results/metrics_summary.json", "w") as f:
        json.dump(all_results, f, indent=4, default=str)

    print("\n=== Summary ===")
    print(df[["Settling Time (s)", "RMSE theta (rad)",
              "RMS force (N)", "Saturation %", "Failed (|theta|>pi/2)"]].to_string())
    print("\nAll figures saved to results/figures/")
    print("Project complete!")


if __name__ == "__main__":
    main()
