import numpy as np

def compute_metrics(y_true, y_pred, y_persistence=None):
    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    r2 = 1 - (np.sum((y_true - y_pred)**2) / np.sum((y_true - np.mean(y_true))**2))
    
    metrics = {
        'MAE': mae,
        'RMSE': rmse,
        'R2': r2,
        'Bias': np.mean(y_pred - y_true)
    }
    
    if y_persistence is not None:
        mae_pers = np.mean(np.abs(y_true - y_persistence))
        metrics['MASE'] = mae / mae_pers if mae_pers > 0 else np.inf
        
    return metrics
