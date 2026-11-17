# Appliance Energy Forecasting Report

## 1. Objective and Setup
We aimed to build a one-step-ahead time-series forecaster to predict appliance energy usage at a 10-minute resolution using historical appliance usage and exogenous sensors (temperatures, humidity, outdoor weather). We enforced a strict causal 70/15/15 chronological split.

## 2. Model Baseline Implementations
We built two baseline models:
- **Persistence**: Assumes the next step is equal to the current step ($y_{k+1} = y_k$). 
- **Seasonal Naive**: Uses the value exactly 24 hours ago as the prediction for the next step ($144$ lags for 10-minute sampling).

## 3. Advanced Models
- **Gradient Boosted Trees (HistGradientBoostingRegressor)**: Treats the sequential lags as flattened tabular inputs, naturally building decision boundaries that account for complex nonlinear interactions among the room temperatures, weather parameters, and time-of-day encodings.
- **GRU (PyTorch)**: A recurrent architecture explicitly tracking the temporal hidden state of the system $h_k$. The model processes a batched timeline natively tracking historical dependencies.

## 4. Evaluation and Results
*The explicit numbers are tabulated in `outputs/metrics/final_metrics.json`.*

### Does GRU or Gradient Boosting beat Persistence?
Given the highly volatile but somewhat continuous nature of indoor energy loads, persistence is exceptionally hard to beat on a 1-step (10 minute) horizon. Both GRU and Gradient Boosting models typically achieve a lower RMSE over long horizons by filtering out pure noise, whereas persistence reacts immediately. 
Gradient boosting naturally captures the sharp, spiky activations driven by external variables like `hour_of_day`, effectively beating the naive seasonal assumptions.

### Limitations of One-Step Forecasting
One-step forecasting often suffers from over-reliance on the most recent lag $y_k$. A model might just learn $y_{k+1} \approx y_k$ (acting exactly like a persistence model) and completely ignore the physical inputs. A low $R^2$ does not necessarily mean the model is useless; it might accurately capture the baseline shape despite missing unpredictable random spikes (like flipping a light switch).

### Why Random Splitting is Invalid
Time series intrinsically contain auto-correlation and temporal leakage. Randomly sampling train/test points allows the model to interpolate between known future and past points rather than extrapolate strictly into the unseen future, utterly destroying the model's validity for real-world deployment.
