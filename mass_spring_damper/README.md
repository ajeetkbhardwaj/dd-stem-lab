# Project 2: Mass-Spring-Damper: Newton’s Law to State Space, Transfer Function, and Integration Comparison

We are going to do modeling for a forced mass-spring-damper system. The goal is to derive the model from Newton’s law, express it in state-space and transfer-function forms, simulate its response, and rigorously compare numerical integration methods.

### Physical system

A mass $m$ moves horizontally and is connected to a fixed wall by a spring of stiffness $k$ and a damper with damping coefficient $c$. An external force $u(t)$ acts on the mass.

The physical equation is:

$$
m\ddot{x}+c\dot{x}+kx=u(t).
$$

Use these baseline parameters:

$$
m=2.0\text{ kg},
\qquad
c=4.0\text{ N}\cdot\text{s/m},
\qquad
k=20.0\text{ N/m}.
$$

Use initial conditions:

$$
x(0)=0\text{ m},
\qquad
\dot{x}(0)=0\text{ m/s}.
$$

Use a step input:

$$
u(t)=
\begin{cases}
0, & t<0,\\
10\text{ N}, & t\geq0.
\end{cases}
$$

Simulate from $t=0$ to $t=10$ s.

### Part A: Derivation from Newton’s law

1. Draw and describe the free-body diagram.
2. Identify all forces:
   - Spring force $F_s=-kx$
   - Damping force $F_d=-c\dot{x}$
   - Applied force $F_a=u(t)$
3. Apply Newton’s second law:

$$
\sum F=m\ddot{x}.
$$

4. Derive:

$$
m\ddot{x}+c\dot{x}+kx=u(t).
$$

5. Substitute the numerical parameters:

$$
2\ddot{x}+4\dot{x}+20x=u(t).
$$

6. Divide by $m$:

$$
\ddot{x}+2\dot{x}+10x=0.5u(t).
$$

### Part B: State-space model

Define:

$$
x_1=x,
\qquad
x_2=\dot{x}.
$$

Derive:

$$
\dot{x}_1=x_2,
$$

$$
\dot{x}_2=-\frac{k}{m}x_1-\frac{c}{m}x_2+\frac{1}{m}u.
$$

Write the state-space model:

$$
\dot{x}=Ax+Bu,
$$

$$
y=Cx+Du,
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
\end{bmatrix},
\qquad
D=0.
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
\end{bmatrix}.
$$

### Part C: Transfer function

Take the Laplace transform assuming zero initial conditions:

$$
(ms^2+cs+k)X(s)=U(s).
$$

Derive:

$$
G(s)=

\frac{1}{ms^2+cs+k}.
$$

For the numerical parameters:

$$
G(s)=\frac{0.5}{s^2+2s+10}.
$$

Write this in standard second-order form:

$$
G(s)=
\frac{\omega_n^2}{s^2+2\zeta\omega_ns+\omega_n^2}.
$$

Compute:

$$
\omega_n=\sqrt{\frac{k}{m}},
$$

$$
\zeta=\frac{c}{2\sqrt{mk}}.
$$

Report:

- Natural frequency $\omega_n$
- Damped natural frequency
- Damping ratio $\zeta$
- Damping type: undamped, underdamped, critically damped, or overdamped
- Poles of the transfer function
- Stability conclusion

### Part D: Analytical response

For the step input $u(t)=10$ for $t\geq0$, compute the steady-state displacement:

$$
x_{ss}(t) = \frac{u_{ss}}{k}.
$$

Explain why:

$$
x_{ss}=\frac{0.5}{\text{ m}}.
$$

For the underdamped case, derive or state the analytical step response:

$$
x(t) = x_{ss}\left[1 - \frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}}\sin\left(\omega_d t + \phi\right)\right],
$$

where:

$$
\omega_d=\omega_n\sqrt{1-\zeta^2},
$$

$$
\phi=
\tan^{-1}
\left(
\frac{\sqrt{1-\zeta^2}}{\zeta}
\right).
$$

Plot the analytical response and numerical response on the same graph.

### Part E: Numerical integration comparison

Implement at least these integration methods from scratch or using SciPy:

1. Explicit Euler
2. Implicit Euler
3. RK4
4. `scipy.integrate.solve_ivp` with `RK45`
5. `scipy.integrate.solve_ivp` with `DOP853`
6. `scipy.integrate.solve_ivp` with `Radau`

For each method, use the state-space form:

$$
\dot{x}=Ax+Bu(t).
$$

Use these fixed step sizes for Euler and RK4:

$$
h\in\{0.1,0.05,0.02,0.01,0.005,0.002,0.001\}\text{ s}.
$$

Use `DOP853` with tight tolerances as the reference solution:

$$
\text{rtol}=10^{-10},
\qquad
\text{atol}=10^{-12}.
$$

For each method and step size, compute:

$$
\mathrm{RMSE}_x = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left(x_{\text{method}}(t_i)-x_{\text{ref}}(t_i)\right)^2}.
$$

Also compute:

$$
\mathrm{MAE}_x = \frac{1}{N}\sum_{i=1}^{N}\left|x_{\text{method}}(t_i)-x_{\text{ref}}(t_i)\right|.
$$

### Part F: Required figures

Create at least these figures:

1. Free-body diagram
2. Position $x(t)$ versus time
3. Velocity $\dot{x}(t)$ versus time
4. Phase portrait: $x$ versus $\dot{x}$
5. Step-response comparison: analytical versus numerical
6. Log-log convergence plot: error versus step size
7. Energy plot for the undamped case
8. Damping comparison: $c=0$, $c=4$, $c=12$, $c=20$

### Part G: Energy analysis

For the undamped case, set $c=0$ and $u(t)=0$.

Compute:

$$
E_k=
\frac{1}{2}m\dot{x}_k^2
+
\frac{1}{2}kx_k^2.
$$

Compare energy conservation for:

- Exact analytical solution
- Explicit Euler
- Implicit Euler
- RK4

Explain why explicit Euler often adds energy in oscillatory systems, while implicit Euler tends to remove energy.

### Required deliverables

Create this repository structure:

```text
mass_spring_damper/
├── README.md
├── requirements.txt
├── src/
│   ├── dynamics.py
│   ├── state_space.py
│   ├── transfer_function.py
│   ├── integrators.py
│   ├── metrics.py
│   └── main.py
├ 
├── results/
│   ├── simulation_truth.csv
│   ├── integration_comparison.csv
│   ├── damping_study.csv
│   ├── figures/
│   └── report.pdf
└── tests/
    └── test_model.py
```

### Required validation checks

code must automatically verify:

1. The state-space $A$ matrix has eigenvalues matching the transfer-function poles.
2. The final simulated position approaches $x_{\text{ss}}=0.5$ m.
3. RK4 error decreases approximately by a factor of 16 when step size is halved.
4. Euler error decreases approximately by a factor of 2 when step size is halved.
5. The undamped analytical and RK4 responses closely match.
6. Damping ratio is correctly classified as underdamped.

### Required report sections

1. System description
2. Assumptions
3. Free-body diagram
4. Newton’s-law derivation
5. State-space derivation
6. Transfer-function derivation
7. Pole and stability analysis
8. Analytical response
9. Numerical-method comparison
10. Damping study
11. Energy conservation
12. Limitations
13. Conclusions

### Acceptance criteria

The project is complete only if:

- The ODE, state-space model, and transfer function are mathematically consistent.
- The analytical and numerical step responses agree.
- The integration study includes quantitative error tables.
- The convergence plot demonstrates expected orders.
- The damping study explains the transition from oscillatory to non-oscillatory behavior.
- All results are reproducible from one command.
