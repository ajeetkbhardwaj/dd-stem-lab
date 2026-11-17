import matplotlib.pyplot as plt

def plot_residuals(y_true, y_pred, model_name, filepath):
    residuals = y_true - y_pred
    plt.figure(figsize=(10, 4))
    plt.plot(residuals.values, alpha=0.7)
    plt.title(f"{model_name} - Residual Time Series")
    plt.xlabel("Test Sample")
    plt.ylabel("Residual (Actual - Predicted)")
    plt.grid()
    plt.savefig(filepath)
    plt.close()

def plot_forecast(y_true, y_pred, model_name, filepath, limit=1008): # 7 days = 1008 samples
    plt.figure(figsize=(12, 5))
    plt.plot(y_true.values[:limit], label='Actual')
    plt.plot(y_pred[:limit], label='Predicted', alpha=0.7)
    plt.title(f"{model_name} - Forecast (First 7 Days)")
    plt.xlabel("Test Sample")
    plt.ylabel("Appliance Energy")
    plt.legend()
    plt.grid()
    plt.savefig(filepath)
    plt.close()
