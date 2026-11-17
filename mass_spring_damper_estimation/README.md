# Project 2: Mass-Spring-Damper State Estimation

## Detailed Prompt

Build a complete state-estimation project for a mass-spring-damper system. The physical model is known from Newton’s law, but only noisy position measurements are available. Your task is to estimate the unmeasured velocity using a Kalman filter and compare it with a Luenberger observer.

### Physical system

A mass $m$ is attached to a spring with stiffness $k$ and damper with damping coefficient $c$. An external force $u(t)$ is applied to the mass.

The equation of motion is:

$$
m\ddot{x}+c\dot{x}+kx=u(t).
$$

Use:

$$
m=2.0\text{ kg},
\qquad
c=4.0\text{ N}\cdot\text{s/m},
\qquad
k=20.0\text{ N/m}.
$$

Use input:

$$
u(t)=10\text{ N}.
$$

Use initial conditions:

$$
x(0)=0\text{ m},
\qquad
\dot{x}(0)=0\text{ m/s}.
$$

### Part A: Derive the physical model

1. Draw the free-body diagram.
2. Identify spring, damping, and applied forces.
3. Apply Newton’s second law:

$$
\sum F=m\ddot{x}.
$$

4. Derive:

$$
m\ddot{x}+c\dot{x}+kx=u(t).
$$

5. Define:

$$
x_1=x,
\qquad
x_2=\dot{x}.
$$

6. Derive the continuous-time state-space model:

$$
\dot{x}=Ax+Bu,
$$

$$
y=Cx+v,
$$

where:

$$
A=
\begin{bmatrix}
0&1\\
-\frac{k}{m}&-\frac{c}{m}
\end{bmatrix},
\qquad
B=
\begin{bmatrix}
0\\
\frac{1}{m}
\end{bmatrix},
$$

$$
C=
\begin{bmatrix}
1&0
\end{bmatrix}.
$$

Substitute numerical values:

$$
A=
\begin{bmatrix}
0&1\\
-10&-2
\end{bmatrix},
\qquad
B=
\begin{bmatrix}
0\\
0.5
\end{bmatrix},
\qquad
C=
\begin{bmatrix}
1&0
\end{bmatrix}.
$$

### Part B: Discretize the system

Use sampling period:

$$
T_s=0.01\text{ s}.
$$

Use zero-order hold discretization:

$$
A_d=e^{AT_s},
$$

$$
B_d=
\int_0^{T_s}e^{A\tau}d\tau B.
$$

Implement the discretization using the matrix exponential:

$$
\begin
A_d&B_d\\
0&I
\end
= 

\exp
\left[
\begin{bmatrix}
A&B\\
0&0
\end{bmatrix}T_s
\right].
$$

Verify that:

$$
A_d\approx I+AT_s+\frac{1}{2}A^2T_s^2
$$

for small $T_s$.

### Part C: Generate noisy measurements

Simulate the true system with process disturbance:

$$
x_{k+1}=A_dx_k+B_du_k+w_k,
$$

where:

$$
w_k\sim\mathcal{N}(0,Q).
$$

Use:

$$
Q=
\begin{bmatrix}
10^{-8}&0\\
0&10^{-6}
\end{bmatrix}.
$$

Measure only position:

$$
y_k=x_{1,k}+v_k,
$$

where:

$$
v_k\sim\mathcal{N}(0,R),
\qquad
R=0.0025.
$$

Thus, the position-measurement standard deviation is:

$$
\sigma_y=0.05\text{ m}.
$$

### Part D: Observability analysis

Compute the observability matrix:

$$
\mathcal{O}=
\begin{bmatrix}
C\\
CA
\end{bmatrix}.
$$

Show that:

$$
\mathcal{O}=
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix}.
$$

Therefore:

$$
\operatorname{rank}(\mathcal{O})=2=n.
$$

Conclude that the system is fully observable and that velocity can be estimated from position measurements.

### Part E: Design a Luenberger observer

Design a continuous-time Luenberger observer:

$$
\dot}
=====

A\hat{x}+Bu+L(y-C\hat{x}).
$$

The observer error is:

$$
e=x-\hat{x}.
$$

Derive:

$$
\dot{e}=(A-LC)e.
$$

Choose observer poles:

$$
\lambda_{o1,2}=-20\pm20i.
$$

Compute observer gain $L$ such that:

$$
\operatorname{eig}(A-LC)=\{-20+20i,-20-20i\}.
$$

Report:

$$
L=
\begin{bmatrix}
l_1\\
l_2
\end{bmatrix}.
$$

### Part F: Design a Kalman filter

Implement the discrete-time Kalman filter:

Prediction:

$$
\hat_
=====

A_d\hat{x}_{k-1|k-1}
+
B_du_{k-1},
$$

$$
P_
==

A_dP_{k-1|k-1}A_d^T+Q.
$$

Update:

$$
K_k
===

P_{k|k-1}C^T
(CP_{k|k-1}C^T+R)^{-1},
$$

$$
\hat_
=====

\hat{x}_{k|k-1}
+
K_k(y_k-C\hat{x}_{k|k-1}),
$$

$$
P_
==

(I-K_kC)P_{k|k-1}.
$$

Use initial conditions:

$$
\hat{x}_{0|0}=
\begin{bmatrix}
0\\
0
\end{bmatrix},
\qquad
P_{0|0}=100I.
$$

### Part G: Compare estimation performance

For both observer and Kalman filter, compute:

$$
\text_}
=======

\sqrt{
\frac{1}{N}
\sum_{k=1}^{N}
(\dot{x}_k-\hat{\dot{x}}_k)^2
},
$$

$$
\text_}
=======

\frac{1}{N}
\sum_{k=1}^{N}
|\dot{x}_k-\hat{\dot{x}}_k|.
$$

Also compute:

- Position estimation RMSE
- Velocity estimation RMSE
- Velocity estimation MAE
- Maximum absolute velocity error
- Convergence time: first time error remains below $0.05$ m/s
- Estimation bias

### Part H: Required experiments

Run these cases:

| Case | Process noise$Q$ | Measurement noise$R$ | Purpose                                       |
| ---- | -----------------: | ---------------------: | --------------------------------------------- |
| 1    |                Low |                    Low | Ideal sensor case                             |
| 2    |                Low |                   High | Poor sensor case                              |
| 3    |               High |                    Low | Model uncertainty case                        |
| 4    |               High |                   High | Realistic noisy case                          |
| 5    |                Low |                   High | Compare Kalman filter and Luenberger observer |

For each case, create:

1. True position versus measured position
2. True velocity versus estimated velocity
3. Velocity estimation error versus time
4. Kalman-gain evolution
5. Estimation-error covariance trace
6. Histogram of velocity-estimation error

### Part I: Required analysis

Explain:

1. Why velocity cannot be measured directly in this setup.
2. Why the observer can estimate velocity from position history.
3. Why the Kalman filter uses both model prediction and measurement correction.
4. What happens when measurement noise increases.
5. What happens when process noise is underestimated.
6. Why the Kalman gain decreases after initial convergence.
7. Why the Luenberger observer may be preferable when noise statistics are unknown.
8. Why the separation principle allows separate observer and controller design.

### Required deliverables

Create this repository:

```text
mass_spring_damper_estimation/
├── README.md
├── requirements.txt
├── src/
│   ├── dynamics.py
│   ├── discretization.py
│   ├── noise.py
│   ├── kalman_filter.py
│   ├── luenberger_observer.py
│   ├── metrics.py
│   └── main.py
├ 
├── results/
│   ├── true_states.csv
│   ├── measurements.csv
│   ├── kalman_estimates.csv
│   ├── observer_estimates.csv
│   ├── estimation_metrics.csv
│   ├── figures/
│   └── report.pdf
└── tests/
    └── test_estimation.py
```

### Acceptance criteria

The project is complete only if:

- The continuous-time model is correctly derived.
- The discretization is numerically correct.
- The observability matrix is computed and interpreted.
- The Kalman filter and Luenberger observer are both implemented.
- Velocity is estimated from position-only measurements.
- Estimation errors are quantitatively compared.
- Noise-sensitivity experiments are included.
- The report explains the trade-off between model trust and measurement trust.

---
