from sklearn.ensemble import HistGradientBoostingRegressor
import numpy as np

def train_gradient_boosting(X_train, y_train, X_val, y_val):
    # LightGBM/HistGradientBoostingRegressor is fast and handles tabular features well
    model = HistGradientBoostingRegressor(max_iter=100, max_depth=5, learning_rate=0.1, l2_regularization=0.1, random_state=42)
    model.fit(X_train, y_train)
    return model
