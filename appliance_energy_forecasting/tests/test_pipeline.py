import pytest
import numpy as np
import pandas as pd
from src.baselines import persistence_forecast

def test_persistence():
    y_hist = np.array([10, 20, 30])
    preds = persistence_forecast(y_hist)
    assert np.allclose(preds, [10, 20, 30])
