import numpy as np

def compute_metrics(true_state, estimated_state, Ts=0.01, threshold=0.05):
    pos_err = true_state[:, 0] - estimated_state[:, 0]
    vel_err = true_state[:, 1] - estimated_state[:, 1]
    
    pos_rmse = np.sqrt(np.mean(pos_err**2))
    vel_rmse = np.sqrt(np.mean(vel_err**2))
    vel_mae  = np.mean(np.abs(vel_err))
    vel_max  = np.max(np.abs(vel_err))
    bias     = np.mean(estimated_state[:, 1] - true_state[:, 1])
    
    # Convergence time: first index where |vel_err| stays below threshold
    below = np.abs(vel_err) < threshold
    conv_idx = None
    for i in range(len(below)):
        if np.all(below[i:i+100]):  # stays below for 1 second
            conv_idx = i
            break
    conv_time = conv_idx * Ts if conv_idx is not None else float('inf')
    
    return {
        'Position RMSE': pos_rmse,
        'Velocity RMSE': vel_rmse,
        'Velocity MAE':  vel_mae,
        'Max Velocity Error': vel_max,
        'Velocity Bias': bias,
        'Convergence Time (s)': conv_time
    }
