# Project 1: UCI Appliances Energy Forecasting

## Detailed Prompt

We will build a complete black-box time-series forecasting system using the UCI Appliances Energy Prediction dataset. The objective is to predict appliance energy consumption for the next 10-minute interval using only information available at or before the current time.

### Dataset

Use the UCI Appliances Energy Prediction dataset:

- Target: `Appliances`
- Sampling interval: 10 minutes
- Approximately 19,735 observations
- Includes appliance energy, light energy, indoor temperature/humidity from nine rooms, outdoor weather variables, and timestamps. [archive.ics.uci](https://archive.ics.uci.edu/datasets?Task=Regression&skip=0&take=10&orderBy=NumHits&Types=Time-Series)

Download the dataset as:

```text
./data/energydata_complete.csv
```

### Forecasting problem

Let:

$$
y_k=\text{Appliances energy at time }k.
$$

Build one-step-ahead forecasting models:

$$
\hat{y}_{k+1} = f_\theta(y_k, y_{k-1}, \ldots, y_{k-L+1}, z_k, z_{k-1}, \ldots, z_{k-L+1}),
$$

where $z_k$ contains observed exogenous variables such as room temperature, humidity, outdoor weather, lighting, and cyclic time features.

The target is always:

$$
y_{k+1}.
$$

You must never use $y_{k+1}$ as an input feature.

### Required models

Implement and compare these four models:

| Model                  | Type                      | Required purpose                                                                  |
| ---------------------- | ------------------------- | --------------------------------------------------------------------------------- |
| Persistence            | Baseline                  | $\hat{y}_{k+1}=y_k$                                                             |
| Seasonal naive         | Baseline                  | $\hat{y}_{k+1}=y_{k+1-144}$, because $24\text{ hours}\times6=144$ samples/day |
| Gradient-boosted trees | Nonlinear tabular ML      | Use engineered lag features and exogenous variables                               |
| GRU                    | Sequential neural network | Learn temporal dependencies and a hidden state                                    |

### Required data preparation

1. Parse the `date` column as a timestamp.
2. Sort observations chronologically.
3. Remove duplicate timestamps.
4. Audit the sampling interval.
5. Check missing values, negative target values, and physically invalid sensor readings.
6. Use only causal information at prediction time.
7. Create cyclic time features:

$$
\text{hour\_sin}=\sin\left(\frac{2\pi h}{24}\right),
$$

$$
\text{hour\_cos}=\cos\left(\frac{2\pi h}{24}\right),
$$

$$
\text{dow\_sin}=\sin\left(\frac{2\pi d}{7}\right),
$$

$$
\text{dow\_cos}=\cos\left(\frac{2\pi d}{7}\right).
$$

8. Include past target values as input features:

$$
y_k,y_{k-1},\ldots,y_{k-L+1}.
$$

Use a history window of:

$$
L=36
$$

samples, corresponding to the previous 6 hours.

9. Include exogenous variables:

- `lights`
- `T1` through `T9`
- `RH_1` through `RH_9`
- `T_out`
- `Press_mm_hg`
- `RH_out`
- `Windspeed`
- `Visibility`
- `Tdewpoint`

10. Exclude `rv1` and `rv2` because they are random variables and are not physically meaningful predictors.

### Required chronological split

Use a chronological split:

$$
\text{Train}=70\%,\qquad
\text{Validation}=15\%,\qquad
\text{Test}=15\%.
$$

Rules:

- Fit all scalers, encoders, and feature transformations on training data only.
- Apply the same fitted transformations to validation and test data.
- Assign each supervised sample to train/validation/test according to the timestamp of its target $y_{k+1}$.
- Allow validation and test windows to use strictly earlier historical observations.
- Never shuffle time-series samples before splitting.
- Never use future target values in the input window.

### Required GRU architecture

Implement a GRU model in PyTorch:

```text
Input: [batch, sequence_length=36, features]
GRU hidden size: 64
Dense layer: 32 units, ReLU
Output: 1 value
Loss: Huber loss
Optimizer: AdamW
```

Use:

$$
h_k=\Phi_\theta(h_{k-1},\xi_k),
$$

$$
\hat{y}_{k+1}=\Psi_\theta(h_k).
$$

The GRU hidden state $h_k$ is a learned black-box latent state. It is not required to have a physical interpretation.

### Required gradient-boosted model

Use `XGBoost`, `LightGBM`, or `HistGradientBoostingRegressor`.

For the gradient-boosted model:

- Use the same causal lag features as the GRU.
- Flatten the lag window into tabular features.
- Tune at least:
  - Number of estimators
  - Maximum depth or leaf count
  - Learning rate
  - Regularization parameter
- Use validation data for hyperparameter selection.
- Evaluate only once on the untouched test set after model selection.

### Required metrics

Compute the following metrics for each model on the test set:

$$
\mathrm{MAE} = \frac{1}{N}\sum_{k=1}^{N}\left|y_k - \hat{y}_k\right|,
$$

$$
\mathrm{RMSE} = \sqrt{\frac{1}{N}\sum_{k=1}^{N}\left(y_k - \hat{y}_k\right)^2},
$$

$$
R^2 = 1 - \frac{\sum_{k=1}^{N}\left(y_k - \hat{y}_k\right)^2}{\sum_{k=1}^{N}\left(y_k - \bar{y}\right)^2},
$$

$$
\mathrm{MASE} = \frac{\mathrm{MAE}_{\text{model}}}{\mathrm{MAE}_{\text{persistence}}}.
$$

Also compute:

- Bias: $\frac{1}{N}\sum(\hat{y}_k-y_k)$
- MAPE on nonzero targets
- Peak-event MAE and RMSE
- Percentage of high-load events detected
- Residual mean and standard deviation

### Required residual diagnostics

For the best model, create:

1. Residual time-series plot:

$$
e_k=y_k-\hat{y}_k.
$$

2. Residual histogram.
3. Residual autocorrelation plot.
4. Residual versus predicted-value scatter plot.
5. Residual versus hour-of-day plot.
6. Residual versus actual energy level.
7. Rolling 24-hour MAE plot.
8. Actual versus predicted scatter plot.
9. Forecast plot for the first seven test days.
10. Failure-case analysis: identify the 10 largest absolute residuals and explain possible causes.

### Required baseline comparison

Your report must answer:

1. Does the GRU beat persistence?
2. Does the GRU beat seasonal naive?
3. Does gradient boosting beat persistence?
4. Which model is best for low-energy periods?
5. Which model is best for high-energy peaks?
6. Does a low $R^2$ necessarily mean the model is useless?
7. What are the limitations of one-step forecasting?
8. Why is random train/test splitting invalid for time-series forecasting?

### Required deliverables

Create this repository structure:

```text
appliance_energy_forecasting/
├── README.md
├── requirements.txt
├── data/
│   └── energydata_complete.csv
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── baselines.py
│   ├── gradient_boosting.py
│   ├── gru_model.py
│   ├── evaluation.py
│   ├── plotting.py
│   └── main.py
├ 
├── outputs/
│   ├── models/
│   ├── predictions/
│   ├── metrics/
│   ├── figures/
│   └── report.pdf
└── tests/
    └── test_pipeline.py
```

### Required outputs

The program must save:

1. Cleaned dataset
2. Feature names and configuration
3. Fitted scaler
4. Trained gradient-boosting model
5. Trained GRU weights
6. Training history
7. Test predictions for all models
8. Residuals for all models
9. Metrics table
10. All figures
11. Final JSON metrics summary

### Acceptance criteria

The project is complete only if:

- The chronological split is correct.
- No future information leaks into model inputs.
- Persistence and seasonal-naive baselines are implemented.
- Gradient boosting and GRU are trained and evaluated.
- MAE, RMSE, $R^2$, and MASE are reported for all models.
- Residual diagnostics are included.
- The best model is selected using validation data only.
- Test evaluation is performed exactly once after model selection.
- The report explains both numerical results and limitations.
