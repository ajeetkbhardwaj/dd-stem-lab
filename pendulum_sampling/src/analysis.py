import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.measurement import generate_measurements, reconstruct_velocity

def sampling_study(t_truth, theta_truth, omega_truth, sampling_periods, sigma_theta=0.01, save_dir=None):
    results = []
    
    for Ts in sampling_periods:
        fs = 1.0 / Ts
        fN = fs / 2.0
        
        t_k, theta_k, theta_k_true = generate_measurements(t_truth, theta_truth, Ts, sigma_theta)
        omega_k_est = reconstruct_velocity(t_k, theta_k)
        
        # True values at sample times
        omega_k_true = np.interp(t_k, t_truth, omega_truth)
        
        mae_pos = np.mean(np.abs(theta_k - theta_k_true))
        rmse_pos = np.sqrt(np.mean((theta_k - theta_k_true)**2))
        
        mae_vel = np.mean(np.abs(omega_k_est - omega_k_true))
        rmse_vel = np.sqrt(np.mean((omega_k_est - omega_k_true)**2))
        
        aliasing = "Yes" if fN < 1.0 else "No"  # Approximate check, natural freq is around 0.5 Hz
        
        results.append({
            "Sampling period": Ts,
            "Sampling frequency": fs,
            "Nyquist frequency": fN,
            "Position MAE": mae_pos,
            "Position RMSE": rmse_pos,
            "Velocity MAE": mae_vel,
            "Velocity RMSE": rmse_vel,
            "Aliasing observed?": aliasing
        })
        
        # Optional plotting
        if save_dir:
            plt.figure(figsize=(10, 5))
            plt.plot(t_truth, theta_truth, label='Truth $\\theta(t)$', alpha=0.7)
            plt.plot(t_k, theta_k, 'rx', label='Sampled $\\theta_k$')
            plt.plot(t_k, theta_k, 'r--', alpha=0.5, label='Reconstructed')
            plt.xlabel('Time [s]')
            plt.ylabel('Angle [rad]')
            plt.title(f'Sampling with Ts = {Ts} s')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"{save_dir}/sampling_Ts_{Ts}.png", dpi=150)
            plt.close()
            
    df = pd.DataFrame(results)
    return df
