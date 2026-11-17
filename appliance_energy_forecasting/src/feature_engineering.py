import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def engineer_features(df, L=36):
    df = df.copy()
    
    # Cyclic time features
    df['hour_sin'] = np.sin(2 * np.pi * df['date'].dt.hour / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['date'].dt.hour / 24.0)
    df['dow_sin'] = np.sin(2 * np.pi * df['date'].dt.dayofweek / 7.0)
    df['dow_cos'] = np.cos(2 * np.pi * df['date'].dt.dayofweek / 7.0)
    
    # Lag features
    for lag in range(1, L + 1):
        df[f'y_lag_{lag}'] = df['Appliances'].shift(lag)
        
    df = df.dropna().reset_index(drop=True)
    
    # Chronological Split: 70% Train, 15% Val, 15% Test
    n = len(df)
    train_end = int(n * 0.7)
    val_end = int(n * 0.85)
    
    train_df = df.iloc[:train_end]
    val_df = df.iloc[train_end:val_end]
    test_df = df.iloc[val_end:]
    
    # Setup X and y
    target = 'Appliances'
    exclude_cols = ['date', target]
    features = [c for c in df.columns if c not in exclude_cols]
    
    X_train, y_train = train_df[features], train_df[target]
    X_val, y_val = val_df[features], val_df[target]
    X_test, y_test = test_df[features], test_df[target]
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    return {
        'X_train': X_train_scaled, 'y_train': y_train,
        'X_val': X_val_scaled, 'y_val': y_val,
        'X_test': X_test_scaled, 'y_test': y_test,
        'features': features, 'scaler': scaler
    }
