# Project 3: Cart-Pole Control: PID, LQR, and MPC

## Detailed Prompt

Design, simulate, and compare PID, LQR, and MPC controllers for a cart-pole inverted-pendulum system. The goal is to stabilize the pendulum upright while respecting actuator saturation and handling measurement noise.

The cart-pole is a canonical unstable, underactuated nonlinear control benchmark; PID, LQR, Kalman filtering, and LQG are commonly compared on this system.

### Physical system

A cart of mass $M$ moves horizontally under force $u(t)$. A pendulum of mass $m_p$ and length $l$ is attached to the cart. The pendulum angle $\theta$ is measured from the upright vertical position.

Use nonlinear equations of motion:

$$
(M+m)\ddot
+
m_p l\ddot\cos\theta
--------------------

m_pl\dot^2\sin\theta
= 

u,
$$

$$
l\ddot
+
\ddot\cos\theta
---------------

g\sin\theta
=
$$

Use parameters:

$$
M=1.0\text{ kg},
\qquad
m_p=0.1\text{ kg},
\qquad
l=0.5\text{ m},
\qquad
g=9.81\text{ m/s}^2.
$$

### Control objective

Starting near the upright equilibrium:

$$
x=0,
\qquad
\dot{x}=0,
\qquad
\theta=0,
\qquad
\dot{\theta}=0,
$$

stabilize the pendulum upright while returning the cart to $x=0$.

Use initial condition:

$$
x(0)=0,
\qquad
\dot{x}(0)=0,
\qquad
\theta(0)=0.10\text{ rad},
\qquad
\dot{\theta}(0)=0.
$$

The control objective is:

$$
x(t)\rightarrow0,
\qquad
\theta(t)\rightarrow0.
$$

### Actuator and sensor constraints

Use actuator saturation:

$$
|u(t)|\leq u_{\max}=20\text{ N}.
$$

Measure:

$$
y=
\begin{bmatrix}
x\\
\theta
\end{bmatrix}
+
v,
$$

where:

$$
v\sim\mathcal{N}(0,R_y),
\qquad
R_y=
\begin{bmatrix}
0.0001&0\\
0&0.0004
\end{bmatrix}.
$$

Thus:

$$
\sigma_x=0.01\text{ m},
\qquad
\sigma_\theta=0.02\text{ rad}.
$$

### Part A: Nonlinear simulation

Implement the nonlinear cart-pole dynamics:

$$
\dot{x}_1=x_2,
$$

$$
\dot{x}_2=f_x(x,u),
$$

$$
\dot{x}_3=x_4,
$$

$$
\dot{x}_4=f_\theta(x,u),
$$

where:

$$
x=
\begin{bmatrix}
x\\
\dot{x}\\
\theta\\
\dot{\theta}
\end{bmatrix}.
$$

Solve the two acceleration equations analytically or numerically at every time step.

Implement:

- `nonlinear_dynamics(state, force)`
- `simulate_nonlinear(initial_state, controller, duration)`
- Actuator saturation
- Measurement-noise generation
- Disturbance injection

### Part B: Linearize around upright equilibrium

The upright equilibrium is:

$$
x^*=
\begin{bmatrix}
0\\
0\\
0\\
0
\end{bmatrix},
\qquad
u^*=0.
$$

Linearize:

$$
\delta\dot
==========

A\delta x+B\delta u.
$$

Compute:

$$
A=
\left.
\frac{\partial f}{\partial x}
\right|_{x^*,u^*},
\qquad
B=
\left.
\frac{\partial f}{\partial u}
\right|_{x^*,u^*}.
$$

Use the standard linearized cart-pole model:

$$
A=
\begin{bmatrix}
0&1&0&0\\
0&0&-\frac{m_pg}{M}&0\\
0&0&0&1\\
0&0&\frac{(M+m_p)g}{Ml}&0
\end{bmatrix},
$$

$$
B=
\begin{bmatrix}
0\\
\frac{1}{M}\\
0\\
-\frac{1}{Ml}
\end{bmatrix}.
$$

Verify:

- Eigenvalues of open-loop $A$
- Instability of the upright equilibrium
- Controllability matrix rank:

$$
\operatorname{rank}
\begin{bmatrix}
B&AB&A^2B&A^3B
\end{bmatrix}
=4.
$$

### Part C: PID controller

Design a PID controller for pendulum angle:

$$
u_}(t)
======

K_p e_\theta(t)
+
K_i\int_0^te_\theta(\tau)d\tau
+
K_d\dot{e}_\theta(t),
$$

where:

$$
e_\theta(t)=\theta_{\text{ref}}-\theta(t).
$$

Use:

$$
\theta_{\text{ref}}=0.
$$

Tune PID gains manually or using a grid search:

$$
K_p\in[10,100],
\qquad
K_i\in[0,20],
\qquad
K_d\in[1,50].
$$

Apply saturation:

$$
u(t)=
\operatorname{clip}(u_{\text{PID}}(t),-20,20).
$$

Explain limitations:

- PID controls only pendulum angle.
- It does not directly regulate cart position.
- Integral action may worsen instability or cause windup.
- Saturation can destroy linear-design assumptions.

### Part D: LQR controller

Design full-state feedback:

$$
u(t)=-Kx(t).
$$

Use LQR cost:

$$
J=
\int_0^\infty
\left(
x^TQx+u^TRu
\right)dt.
$$

Use:

$$
Q=
\operatorname{diag}(10,1,100,1),
\qquad
R=1.
$$

Solve the continuous-time algebraic Riccati equation:

$$
A^TP+PA-PBR^{-1}B^TP+Q=0.
$$

Compute:

$$
K=R^{-1}B^TP.
$$

Test at least three LQR tunings:

| Case         | $Q$                                   | $R$ | Expected behavior            |
| ------------ | --------------------------------------- | ----: | ---------------------------- |
| Conservative | $\operatorname{diag}(1,0.1,10,0.1)$   |    10 | Slower, lower control effort |
| Baseline     | $\operatorname{diag}(10,1,100,1)$     |     1 | Balanced                     |
| Aggressive   | $\operatorname{diag}(100,10,1000,10)$ |   0.1 | Fast, high control effort    |

For each tuning, report:

- Closed-loop eigenvalues
- Settling time
- Maximum pendulum angle
- Maximum cart displacement
- Maximum control effort
- Percentage of time saturated
- RMS control effort
- Robustness to measurement noise

### Part E: MPC controller

Implement a discrete-time MPC controller.

First discretize the linearized system using:

$$
T_s=0.02\text{ s}.
$$

Use:

$$
x_{k+1}=A_dx_k+B_du_k.
$$

At each time step, solve:

$$
\min_{u_0,\ldots,u_{H-1}}
\sum_{j=1}^{H}
x_j^TQx_j
+
\sum_{j=0}^{H-1}
u_j^TRu_j
$$

subject to:

$$
x_{j+1}=A_dx_j+B_du_j,
$$

$$
|u_j|\leq20,
$$

$$
|x_j|\leq2.0\text{ m},
$$

$$
|\theta_j|\leq0.35\text{ rad}.
$$

Use prediction horizon:

$$
H\in\{10,20,30\}.
$$

Use only the first control action:

$$
u_k=u_0^*.
$$

Then move to the next time step and repeat.

Implement MPC using:

- `cvxpy`
- `osqp`
- `scipy.optimize`
- Or a custom quadratic-programming solver

### Part F: Measurement-noise experiments

For each controller, run simulations with noisy measurements:

$$
y_k=
\begin{bmatrix}
x_k\\
\theta_k
\end{bmatrix}
+
v_k.
$$

For PID and LQR, use noisy measurements directly.

For MPC, either:

- Use noisy full-state measurements, or
- Add a Kalman filter to estimate the full state from $x$ and $\theta$.

Run at least 20 Monte Carlo simulations per controller with different random seeds.

Report:

- Mean settling time
- Standard deviation of settling time
- Mean maximum control effort
- Saturation percentage
- Failure rate: pendulum falls beyond $|\theta|>0.35$ rad
- Mean absolute cart displacement
- Mean RMSE tracking error

### Part G: Required comparisons

Create a final comparison table:

| Controller | Stabilizes upright? | Handles cart position? | Uses constraints? | Noise robustness | Saturation behavior | Best use case |
| ---------- | ------------------: | ---------------------: | ----------------: | ---------------- | ------------------- | ------------- |
| PID        |                     |                        |                   |                  |                     |               |
| LQR        |                     |                        |                   |                  |                     |               |
| MPC        |                     |                        |                   |                  |                     |               |

Explain:

1. Why the cart-pole is unstable.
2. Why PID alone cannot fully solve the multivariable problem.
3. Why LQR requires full-state feedback.
4. Why MPC naturally handles constraints.
5. Why actuator saturation can destabilize an aggressive LQR controller.
6. Why measurement noise can be amplified by high-gain feedback.
7. Why MPC may be preferable when constraints are important.
8. Why a Kalman filter or observer is needed for practical implementation.

### Required deliverables

Create this repository:

```text
cart_pole_control/
├── README.md
├── requirements.txt
├── src/
│   ├── cart_pole_dynamics.py
│   ├── linearization.py
│   ├── pid_controller.py
│   ├── lqr_controller.py
│   ├── mpc_controller.py
│   ├── kalman_filter.py
│   ├── simulation.py
│   ├── metrics.py
│   └── main.py
├ 
├── results/
│   ├── pid_results.csv
│   ├── lqr_results.csv
│   ├── mpc_results.csv
│   ├── noise_results.csv
│   ├── figures/
│   └── report.pdf
└── tests/
    └── test_controllers.py
```

### Required figures

Create at least these plots:

1. Open-loop unstable response
2. PID angle and cart-position response
3. LQR angle and cart-position response
4. MPC angle and cart-position response
5. Control-effort comparison
6. Saturation comparison
7. Phase portrait: $\theta$ versus $\dot{\theta}$
8. Phase portrait: $x$ versus $\dot{x}$
9. Measurement-noise robustness comparison
10. MPC constraint-activation plot
11. LQR tuning comparison
12. Monte Carlo performance boxplots

### Required validation checks

the code must automatically verify:

1. The nonlinear model conserves physical consistency.
2. The open-loop linearized system is unstable.
3. The controllability matrix has full rank.
4. LQR closed-loop eigenvalues have negative real parts.
5. MPC respects actuator and state constraints.
6. PID saturation is applied correctly.
7. The nonlinear simulation runs without divergence for all controllers.
8. Monte Carlo results include multiple random seeds.

### Required report sections

1. System description
2. Nonlinear dynamics derivation
3. Linearization
4. Controllability and instability analysis
5. PID design and limitations
6. LQR design and tuning
7. MPC formulation and constraints
8. Measurement-noise model
9. Simulation results
10. Controller comparison
11. Saturation and robustness analysis
12. Limitations
13. Recommendations for real hardware
14. Conclusions

### Acceptance criteria

The project is complete only if:

- The nonlinear cart-pole simulator is correct.
- PID, LQR, and MPC are all implemented.
- Actuator saturation is enforced in every controller.
- Measurement noise is included.
- LQR is tested with at least three tunings.
- MPC enforces constraints explicitly.
- Monte Carlo noise experiments are included.
- The report compares performance, robustness, and practical limitations.

---
