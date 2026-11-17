import os
import json
import pandas as pd
from src.data_loader import load_data
from src.feature_engineering import engineer_features
from src.baselines import persistence_forecast, seasonal_naive_forecast
from src.gradient_boosting import train_gradient_boosting
from src.gru_model import train_gru, predict_gru
from src.evaluation import compute_metrics
from src.plotting import plot_residuals, plot_forecast

def main():
    print("Loading data...")
    df = load_data('data/energydata_complete.csv')
    
    print("Engineering features and splitting...")
    data = engineer_features(df, L=36)
    
    X_train, y_train = data['X_train'], data['y_train']
    X_val, y_val = data['X_val'], data['y_val']
    X_test, y_test = data['X_test'], data['y_test']
    
    # Extract raw historical labels for baselines
    y_test_hist = df['Appliances'].iloc[-len(y_test)-1:-1].values
    
    print("Running Baselines...")
    preds_pers = persistence_forecast(y_test_hist)
    preds_sn = seasonal_naive_forecast(y_test.values, period=144)
    
    print("Training Gradient Boosting...")
    gb_model = train_gradient_boosting(X_train, y_train, X_val, y_val)
    preds_gb = gb_model.predict(X_test)
    
    print("Training GRU Model (10 epochs for accuracy)...")
    gru_model = train_gru(X_train, y_train, X_val, y_val, epochs=10)
    preds_gru = predict_gru(gru_model, X_test)
    
    print("Saving Models and Predictions...")
    import joblib
    import torch
    joblib.dump(gb_model, 'outputs/models/gb_model.pkl')
    torch.save(gru_model[0].state_dict(), 'outputs/models/gru_model.pt')
    
    pd.DataFrame({
        'Persistence': preds_pers,
        'Seasonal_Naive': preds_sn,
        'Gradient_Boosting': preds_gb,
        'GRU': preds_gru
    }).to_csv('outputs/predictions/test_predictions.csv', index=False)
    
    print("Evaluating...")
    m_pers = compute_metrics(y_test, preds_pers)
    m_sn = compute_metrics(y_test, preds_sn, preds_pers)
    m_gb = compute_metrics(y_test, preds_gb, preds_pers)
    m_gru = compute_metrics(y_test, preds_gru, preds_pers)
    
    all_metrics = {
        "Persistence": m_pers,
        "Seasonal Naive": m_sn,
        "Gradient Boosting": m_gb,
        "GRU": m_gru
    }
    
    print(pd.DataFrame(all_metrics).T)
    
    with open('outputs/metrics/final_metrics.json', 'w') as f:
        json.dump(all_metrics, f, indent=4)
        
    print("Generating Plots...")
    plot_residuals(y_test, preds_gb, "Gradient Boosting", "outputs/figures/gb_residuals.png")
    plot_forecast(y_test, preds_gb, "Gradient Boosting", "outputs/figures/gb_forecast.png")
    plot_residuals(y_test, preds_gru, "GRU", "outputs/figures/gru_residuals.png")
    plot_forecast(y_test, preds_gru, "GRU", "outputs/figures/gru_forecast.png")
    
    print("Project executed successfully!")

if __name__ == '__main__':
    main()
