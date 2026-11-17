import numpy as np

def compute_metrics(t, states, forces, Ts=0.02, theta_max=np.pi/2):
    theta   = states[:, 2]
    x_cart  = states[:, 0]

    # Settling: angle stays within 0.05 rad
    settled = np.abs(theta) < 0.05
    settle_idx = None
    for i in range(len(settled)):
        if np.all(settled[i:i+50]):
            settle_idx = i
            break
    settle_time = settle_idx * Ts if settle_idx is not None else float('inf')

    sat = np.sum(np.abs(forces) >= 19.9) / len(forces) * 100

    return {
        "Settling Time (s)":          settle_time,
        "Max |theta| (rad)":          float(np.max(np.abs(theta))),
        "Max |x_cart| (m)":           float(np.max(np.abs(x_cart))),
        "Max |force| (N)":            float(np.max(np.abs(forces))),
        "Saturation %":               float(sat),
        "RMS force (N)":              float(np.sqrt(np.mean(forces**2))),
        "Failed (|theta|>pi/2)":      bool(np.any(np.abs(theta) > theta_max)),
        "RMSE theta (rad)":           float(np.sqrt(np.mean(theta**2))),
    }
