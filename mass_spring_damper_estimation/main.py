import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

from src.dynamics import get_continuous_system, check_observability
from src.discretization import discretize_system
from src.noise import generate_process_noise, generate_measurement_noise
from src.kalman_filter import KalmanFilter
from src.luenberger_observer import LuenbergerObserver, design_observer_gain
from src.metrics import compute_metrics

# ── Parameters ────────────────────────────────────────────────────────────────
m, c, k  = 2.0, 4.0, 20.0
u_val    = np.array([[10.0]])    # constant input force (N)
Ts       = 0.01
T_end    = 10.0
N        = int(T_end / Ts)
t        = np.linspace(0, T_end, N)

x0_true  = np.array([0.0, 0.0])
x0_est   = np.array([0.0, 0.0])
P0       = 100.0 * np.eye(2)


# ── Experiment cases ──────────────────────────────────────────────────────────
cases = {
    "Low Q Low R":  {"Q": np.diag([1e-8, 1e-6]),  "R": np.array([[0.0025]])},
    "Low Q High R": {"Q": np.diag([1e-8, 1e-6]),  "R": np.array([[0.25]])},
    "High Q Low R": {"Q": np.diag([1e-4, 1e-2]),  "R": np.array([[0.0025]])},
    "High Q High R":{"Q": np.diag([1e-4, 1e-2]),  "R": np.array([[0.25]])},
}


def run_case(case_name, Q, R, seed_proc=42, seed_meas=43, compare_observer=False):
    A, B, C = get_continuous_system(m, c, k)
    Ad, Bd  = discretize_system(A, B, Ts=Ts)

    # ── Simulate true system with process noise ────────────────────────────
    w = generate_process_noise(Q, N, seed=seed_proc)
    v = generate_measurement_noise(R, N, seed=seed_meas)

    x_true = np.zeros((N, 2))
    y_meas = np.zeros((N, 1))
    x      = x0_true.copy()

    for k_idx in range(N):
        x_true[k_idx] = x
        y_meas[k_idx] = C @ x + v[k_idx]
        x = Ad @ x + Bd.flatten() * u_val.flatten()[0] + w[k_idx]

    # ── Kalman Filter ──────────────────────────────────────────────────────
    kf = KalmanFilter(Ad, Bd, C, Q, R, x0_est.copy(), P0.copy())
    kf_est = np.zeros((N, 2))

    for k_idx in range(N):
        kf.predict(u_val)
        kf_est[k_idx] = kf.update(y_meas[k_idx])

    # ── Luenberger Observer (only for comparison case) ─────────────────────
    obs_est = None
    if compare_observer:
        L = design_observer_gain(A, C)
        obs = LuenbergerObserver(A, B, C, L, x0_est.copy())
        obs_est = np.zeros((N, 2))
        for k_idx in range(N):
            obs_est[k_idx] = obs.update(y_meas[k_idx], u_val)

    # ── Metrics ────────────────────────────────────────────────────────────
    kf_metrics  = compute_metrics(x_true, kf_est, Ts=Ts)
    obs_metrics = compute_metrics(x_true, obs_est, Ts=Ts) if obs_est is not None else None

    # ── Plots ──────────────────────────────────────────────────────────────
    fname = case_name.lower().replace(" ", "_")
    fig, axes = plt.subplots(3, 1, figsize=(12, 9))

    axes[0].plot(t, x_true[:, 0], label='True Position', linewidth=2)
    axes[0].plot(t, y_meas[:, 0], alpha=0.4, label='Measured Position')
    axes[0].plot(t, kf_est[:, 0], '--', label='KF Position')
    if obs_est is not None:
        axes[0].plot(t, obs_est[:, 0], ':', label='Observer Position')
    axes[0].set_ylabel('Position (m)'); axes[0].legend(); axes[0].grid()
    axes[0].set_title(f'Case: {case_name}')

    axes[1].plot(t, x_true[:, 1], label='True Velocity', linewidth=2)
    axes[1].plot(t, kf_est[:, 1], '--', label='KF Velocity')
    if obs_est is not None:
        axes[1].plot(t, obs_est[:, 1], ':', label='Observer Velocity')
    axes[1].set_ylabel('Velocity (m/s)'); axes[1].legend(); axes[1].grid()

    vel_err_kf = x_true[:, 1] - kf_est[:, 1]
    axes[2].plot(t, vel_err_kf, label='KF Velocity Error')
    if obs_est is not None:
        vel_err_obs = x_true[:, 1] - obs_est[:, 1]
        axes[2].plot(t, vel_err_obs, label='Observer Velocity Error')
    axes[2].axhline(0, color='k', linewidth=0.8)
    axes[2].set_xlabel('Time (s)'); axes[2].set_ylabel('Velocity Error (m/s)')
    axes[2].legend(); axes[2].grid()

    plt.tight_layout()
    plt.savefig(f'results/figures/{fname}.png', dpi=100)
    plt.close()

    # Kalman gain evolution plot
    K_hist = np.array(kf.K_history)
    P_hist = np.array(kf.P_trace_history)
    fig2, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(t[:len(K_hist)], K_hist[:, 0, 0], label='K[position]')
    ax[0].plot(t[:len(K_hist)], K_hist[:, 1, 0], label='K[velocity]')
    ax[0].set_ylabel('Kalman Gain'); ax[0].legend(); ax[0].grid()
    ax[0].set_title(f'Kalman Gain Evolution - {case_name}')
    ax[1].plot(t[:len(P_hist)], P_hist, color='purple')
    ax[1].set_xlabel('Time (s)'); ax[1].set_ylabel('trace(P)')
    ax[1].set_title('Estimation Error Covariance Trace'); ax[1].grid()
    plt.tight_layout()
    plt.savefig(f'results/figures/{fname}_kalman_gain.png', dpi=100)
    plt.close()

    return kf_metrics, obs_metrics


def main():
    print("Checking observability...")
    A, B, C = get_continuous_system(m, c, k)
    is_obs, O = check_observability(A, C)
    print(f"System observable: {is_obs}, rank(O)={np.linalg.matrix_rank(O)}")
    print(f"Observability matrix:\n{O}")

    all_results = []

    for i, (case_name, params) in enumerate(cases.items()):
        compare = (i == 1)   # Compare observer only for Case 2 (Low Q, High R)
        print(f"\nRunning: {case_name} ...")
        kf_m, obs_m = run_case(case_name, params["Q"], params["R"],
                                compare_observer=compare)
        row = {"Case": case_name}
        for metric_name, val in kf_m.items():
            row[f"KF_{metric_name}"] = val
        if obs_m:
            for metric_name, val in obs_m.items():
                row[f"Obs_{metric_name}"] = val
        all_results.append(row)

    # Save metrics
    df = pd.DataFrame(all_results)
    df.to_csv("results/estimation_metrics.csv", index=False)
    print("\n=== Estimation Metrics ===")
    print(df[['Case', 'KF_Velocity RMSE', 'KF_Velocity MAE',
              'KF_Convergence Time (s)']].to_string(index=False))

    # Save JSON summary
    summary = {}
    for row in all_results:
        summary[row["Case"]] = {k: v for k, v in row.items() if k != "Case"}
    with open("results/metrics_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("\nAll figures saved to results/figures/")
    print("Project complete!")


if __name__ == "__main__":
    main()
