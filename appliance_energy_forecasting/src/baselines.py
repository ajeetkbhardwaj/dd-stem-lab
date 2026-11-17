import numpy as np
import pandas as pd

def persistence_forecast(y_history):
    # hat_y_{k+1} = y_k
    return y_history

def seasonal_naive_forecast(y_history, period=144):
    # hat_y_{k+1} = y_{k+1-144}
    # For a simple vectorized implementation on the test set:
    preds = np.roll(y_history, shift=period)
    preds[:period] = y_history[:period] # fallback for the first 'period' elements
    return preds
