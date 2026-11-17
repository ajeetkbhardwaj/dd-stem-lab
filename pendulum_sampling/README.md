# Project 1: Pendulum Simulator, Noisy Measurements, and Sampling Effects

We are going to do a numerical simulation and measurement-analysis for a simple pendulum using Python. The goal is to understand how a continuous physical system is converted into sampled digital measurements, how noise affects those measurements, and how sampling rate affects reconstruction of the true motion.

### Physical system

Model a simple pendulum of length $L$ and mass $m$, with angular displacement $\theta(t)$ measured from the downward vertical position. Assume viscous damping with coefficient $b$, and optionally an externally applied torque $\tau(t)$.

The nonlinear equation of motion is:

$$
mL^2\ddot{\theta}+b\dot{\theta}+mgL\sin\theta=\tau(t).
$$

Use these baseline parameters:

$$
m=1.0\text{ kg},\qquad
L=1.0\text{ m},\qquad
g=9.81\text{ m/s}^2,\qquad
b=0.1\text{ N}\cdot\text{m}\cdot\text{s}.
$$

Use initial conditions:

$$
\theta(0)=1.2\text{ rad},\qquad
\dot{\theta}(0)=0\text{ rad/s}.
$$

### Required mathematical work

1. Define the state vector:

$$
x_1=\theta,\qquad
x_2=\dot{\theta}.
$$

2. Convert the second-order ODE into two first-order ODEs:

$$
\dot{x}_1=x_2,
$$

$$
\dot{x}_2=
-\frac{g}{L}\sin x_1
-\frac{b}{mL^2}x_2
+\frac{1}{mL^2}\tau(t).
$$

3. Derive the undamped small-angle natural frequency:

$$
\omega_0=\sqrt{\frac{g}{L}}.
$$

4. Derive the damped small-angle natural frequency and damping ratio:

$$
\omega_n=\sqrt{\frac{g}{L}},
\qquad
\zeta=
\frac{b}{2mL^2\omega_n}.
$$

5. Explain when the small-angle approximation is valid and when it fails.

### Required simulator

Implement a reusable Python class or module named `PendulumSimulator` with:

- Parameters: $m$, $L$, $g$, $b$
- State: $[\theta,\dot{\theta}]$
- Method: `rhs(t, state, torque)`
- Method: `simulate(t_span, initial_state, torque_function, method, max_step)`
- Support at least these integrators:
  - Fixed-step explicit Euler
  - Fixed-step RK4
  - Adaptive `solve_ivp` with `RK45`
  - Adaptive `solve_ivp` with `DOP853`

The simulator must return a high-resolution “truth” trajectory using a sufficiently small tolerance and dense output.

### Required measurement model

Assume that only the angular position $\theta(t)$ is measured by a digital encoder.

Generate measurements at sampling period $T_s$:

$$
\theta[k]
= 

\theta(t_k)+v_k,
\qquad
t_k=kT_s,
$$

where:

$$
v_k\sim\mathcal{N}(0,\sigma_\theta^2).
$$

Use:

$$
\sigma_\theta=0.01\text{ rad}.
$$

Implement at least these sampling periods:

$$
T_s\in\{0.001,0.005,0.01,0.02,0.05,0.1,0.2,0.5\}\text{ s}.
$$

For each sampling period:

- Compute the sampling frequency $f_s=1/T_s$.
- Compute the Nyquist frequency $f_N=f_s/2$.
- Compare the sampled signal with the high-resolution truth.
- Compute interpolation error after reconstructing the sampled signal.
- Compute MAE and RMSE against the true continuous-time trajectory evaluated at the sample times.
- Plot true $\theta(t)$, sampled points, and reconstructed $\theta(t)$.
- Plot true $\dot{\theta}(t)$, sampled $\theta_k$, and a finite-difference velocity estimate:

$$
\hat{\dot{\theta}}_k
\approx
\frac{\theta_{k+1}-\theta_k}{T_s}.
$$

### Required sampling analysis

Create a table with columns:

| Sampling period | Sampling frequency | Nyquist frequency | Position MAE | Position RMSE | Velocity MAE | Velocity RMSE | Aliasing observed? |
| --------------- | -----------------: | ----------------: | -----------: | ------------: | -----------: | ------------: | ------------------ |

Explain the following:

1. Why very slow sampling produces misleading apparent frequencies.
2. Why the sampled position may look smooth even when velocity reconstruction is poor.
3. Why finite differencing amplifies measurement noise.
4. Why the sampling rate must be substantially higher than the highest dynamics of interest.
5. Why using the exact sample-time values from an adaptive solver is important.

### Required numerical validation

Compare fixed-step Euler and RK4 against the high-accuracy `DOP853` reference solution.

Use step sizes:

$$
h\in\{0.1,0.05,0.02,0.01,0.005,0.002,0.001\}\text{ s}.
$$

For each method, compute:

$$
L({\theta})= 

\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
(\theta_{\text{method}}(t_i)-\theta_{\text{reference}}(t_i))^2
}.
$$

Plot log-log convergence:

$$
\text{RMSE}
\quad\text{versus}\quad
h.
$$

Explain the expected approximate convergence orders:

- Euler: first order
- RK4: fourth order
- Adaptive solver: tolerance-controlled rather than fixed-step-order behavior

### Required energy analysis

For the undamped case, set $b=0$ and $\tau(t)=0$.

Compute total mechanical energy:

$$
E(t)
= 
\frac{1}{2}mL^2\dot{\theta}^2
+
mgL(1-\cos\theta).
$$

Plot energy versus time for:

- Exact/reference integration
- Euler
- RK4

Explain why explicit Euler may cause energy drift, while RK4 should conserve energy much better over a short interval.

### Required deliverables

Create a project repository with:

```text
pendulum_sampling/
├── README.md
├── requirements.txt
├── src/
│   ├── pendulum.py
│   ├── integrators.py
│   ├── measurement.py
│   ├── analysis.py
│   └── main.py
├ 
├── results/
│   ├── truth_simulation.csv
│   ├── sampled_measurements.csv
│   ├── sampling_study.csv
│   ├── integrator_study.csv
│   ├── figures/
│   └── report.pdf
└── tests/
    └── test_pendulum.py
```

### Required report sections

Your final report must include:

1. Physical system description and assumptions
2. Derivation of equations of motion
3. State-space representation
4. Numerical-method descriptions
5. Truth-simulation setup and convergence check
6. Measurement-noise model
7. Sampling study
8. Aliasing analysis
9. Integrator comparison
10. Energy-conservation analysis
11. Limitations and real-world considerations
12. Conclusions

### Acceptance criteria

The project is complete only if:

- The nonlinear ODE is implemented correctly.
- Euler, RK4, `RK45`, and `DOP853` all run successfully.
- The high-resolution reference solution is demonstrably converged.
- Sampling effects are quantified, not merely described.
- The report distinguishes simulation error from measurement noise.
- All figures have labeled axes, legends, titles, and units.
- The code runs end-to-end from a single command.
- No future measurements are used to reconstruct a past measurement.

---
