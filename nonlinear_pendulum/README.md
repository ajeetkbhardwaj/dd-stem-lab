# Project 3: Nonlinear Pendulum: Equilibria, Stability, Phase Portraits, and Damping

## Detailed Prompt

We are going to do nonlinear-dynamics analysis of a pendulum. The goal is to move beyond small-angle approximation and analyze the full nonlinear system: equilibria, stability, phase portraits, oscillations, damping, and energy behavior.

### Physical system

Use the nonlinear pendulum equation:

$$
mL^2\ddot{\theta}+b\dot{\theta}+mgL\sin\theta=\tau(t).
$$

For the main analysis, use:

$$
\tau(t)=0.
$$

Use baseline parameters:

$$
m=1.0\text{ kg},
\qquad
L=1.0\text{ m},
\qquad
g=9.81\text{ m/s}^2.
$$

Use damping values:

$$
b\in\{0.0,0.1,0.5,1.0,2.0,5.0\}
\text{ N}\cdot\text{m}\cdot\text{s}.
$$

### Part A: Convert to first-order form

Define:

$$
x_1=\theta,
\qquad
x_2=\dot{\theta}.
$$

Derive:

$$
\dot{x}_1=x_2,
$$

$$
\dot{x}_2=
-\frac{g}{L}\sin x_1
-\frac{b}{mL^2}x_2
+\frac{\tau(t)}{mL^2}.
$$

For zero torque:

$$
\dot{x}_2=
-\frac{g}{L}\sin x_1
-\frac{b}{mL^2}x_2.
$$

### Part B: Find equilibria

An equilibrium satisfies:

$$
\dot{x}_1=0,
\qquad
\dot{x}_2=0.
$$

Therefore:

$$
x_2^*=0,
$$

$$
-\frac{g}{L}\sin x_1^*=0.
$$

Thus:

$$
x_1^*=n\pi,
\qquad
n\in\mathbb{Z}.
$$

Explain the physical meaning:

- $x_1^*=0$: pendulum hanging downward
- $x_1^*=\pi$: pendulum standing upright
- $x_1^*=-\pi$: same upright configuration, modulo $2\pi$

Because angles are periodic, reduce the analysis to:

$$
\theta\in[-\pi,\pi].
$$

### Part C: Linear stability analysis

Compute the Jacobian:

$$
J(x^*)=
\begin{bmatrix}
0&1\\
-\frac{g}{L}\cos x_1^*&-\frac{b}{mL^2}
\end{bmatrix}.
$$

For the downward equilibrium:

$$
x^*=(0,0),
$$

the Jacobian is:

$$
J_0=
\begin{bmatrix}
0&1\\
-\frac{g}{L}&-\frac{b}{mL^2}
\end{bmatrix}.
$$

Compute eigenvalues:

$$
\lambda_{1,2} = -\frac{b}{2mL^2} \pm \sqrt{\left(\frac{b}{2mL^2}\right)^2 - \frac{g}{L}}.
$$

Classify the equilibrium for each damping value:

| Damping condition       | Classification                |
| ----------------------- | ----------------------------- |
| $b=0$                 | Center                        |
| $0<b<2mL^2\sqrt{g/L}$ | Stable spiral                 |
| $b=2mL^2\sqrt{g/L}$   | Critically damped stable node |
| $b>2mL^2\sqrt{g/L}$   | Overdamped stable node        |

For the upright equilibrium:

$$
x^*=(\pi,0),
$$

show that:

$$
J_\pi=
\begin{bmatrix}
0&1\\
\frac{g}{L}&-\frac{b}{mL^2}
\end{bmatrix}.
$$

Show that one eigenvalue has positive real part for $b\geq0$, so the upright equilibrium is unstable.

### Part D: Energy analysis

For zero damping and zero torque, derive total mechanical energy:

$$
E(\theta,\dot{\theta}) = \frac{1}{2}mL^2\dot{\theta}^2 + mgL(1-\cos\theta).
$$

Show that:

$$
\frac{dE}{dt}=0
$$

when $b=0$.

For $b>0$, show:

$$
\frac{dE}{dt} = -b\dot{\theta}^2 \le 0.
$$

Interpret this result:

- $b=0$: energy is conserved; closed orbits occur.
- $b>0$: energy decreases; trajectories spiral toward the downward equilibrium.

### Part E: Phase portraits

Create phase portraits in the plane:

$$
(\theta,\dot{\theta}).
$$

Use:

$$
\theta\in[-3\pi,3\pi],
\qquad
\dot{\theta}\in[-10,10].
$$

For each damping value, plot:

1. Vector field arrows
2. Multiple trajectories from carefully chosen initial conditions
3. Equilibrium points
4. Stable and unstable manifolds where appropriate
5. Separatrices for the undamped case

Use initial conditions such as:

$$
(\theta_0,\dot{\theta}_0)
\in
\left\{
(0.1,0),
(1.0,0),
(2.0,0),
(3.0,0),
(0,2),
(0,5),
(0,8),
(\pi-0.1,0),
(\pi+0.1,0)
\right\}.
$$

Clearly distinguish:

- Closed orbits: oscillation without crossing the top
- Rotating orbits: full rotations
- Separatrix: boundary between oscillation and rotation
- Spirals: damped oscillations
- Direct approach: overdamped decay

### Part F: Oscillation analysis

For each damping value, simulate from:

$$
(\theta_0,\dot{\theta}_0)=(1.5,0).
$$

Plot:

1. $\theta(t)$ versus time
2. $\dot{\theta}(t)$ versus time
3. Phase trajectory
4. Energy versus time
5. Energy dissipation rate:

$$
-\frac{dE}{dt}=b\dot{\theta}^2.
$$

Compute and report:

- Number of visible oscillations before settling
- Time to remain within $0.01$ rad of the final equilibrium
- Maximum absolute angular velocity
- Final equilibrium
- Whether the pendulum crosses $\theta=\pi$

### Part G: Linear versus nonlinear model

Compare the linearized model:

$$
\ddot{\theta} + \frac{b}{mL^2}\dot{\theta} + \frac{g}{L}\theta = 0
$$

with the nonlinear model:

$$
\ddot{\theta} + \frac{b}{mL^2}\dot{\theta} + \frac{g}{L}\sin\theta = 0.
$$

Use initial angles:

$$
\theta_0\in\{0.1,0.5,1.0,1.5,2.0,2.5,3.0\}\text{ rad}.
$$

For each initial angle, compute the error:

$$
\mathrm{RMSE}_\theta = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left(\theta_{\text{linear}}(t_i)-\theta_{\text{nonlinear}}(t_i)\right)^2}.
$$

Plot RMSE versus initial angle.

Explain:

- Why the linear model works well for small $\theta$
- Why it fails for large $\theta$
- Why the nonlinear pendulum has amplitude-dependent period
- Why the linearized model has constant period

### Part H: Optional driven-pendulum extension

For advanced analysis, add periodic forcing:

$$
\tau(t)=A\cos(\Omega t).
$$

Use:

$$
A\in\{0.5,1.0,1.5,2.0\}\text{ N}\cdot\text{m},
$$

$$
\Omega\in\left\{
\frac{1}{3}\omega_0,
\frac{1}{2}\omega_0,
\omega_0,
\frac{3}{2}\omega_0,
2\omega_0
\right\}.
$$

Investigate:

- Resonance
- Phase locking
- Quasiperiodic behavior
- Possible chaotic behavior
- Poincaré sections
- Lyapunov exponents

Clearly distinguish chaotic behavior from numerical error. Use at least two different tolerances and two different integrators before claiming chaos.

### Required deliverables

Create this repository structure:

```text
nonlinear_pendulum/
├── README.md
├── requirements.txt
├── src/
│   ├── pendulum_dynamics.py
│   ├── equilibrium_analysis.py
│   ├── phase_portrait.py
│   ├── energy_analysis.py
│   ├── linear_vs_nonlinear.py
│   └── main.py
├ 
├── results/
│   ├── equilibria.csv
│   ├── eigenvalues.csv
│   ├── damping_study.csv
│   ├── linear_vs_nonlinear.csv
│   ├── figures/
│   └── report.pdf
└── tests/
    └── test_pendulum_analysis.py
```

### Required validation checks

the code must automatically verify:

1. Equilibria occur at $(n\pi,0)$.
2. The Jacobian at $(0,0)$ matches the analytic expression.
3. For $b=0$, total energy remains approximately constant.
4. For $b>0$, total energy is non-increasing.
5. The downward equilibrium is stable for all $b>0$.
6. The upright equilibrium is unstable for all $b\geq0$.
7. The linear model agrees with the nonlinear model for sufficiently small $\theta_0$.
8. Phase trajectories do not cross in a deterministic autonomous system.

### Required report sections

1. Physical description and assumptions
2. Nonlinear equation of motion
3. First-order state-space form
4. Equilibrium analysis
5. Jacobian and linearization
6. Eigenvalue and stability classification
7. Energy derivation and conservation/dissipation
8. Phase portraits for all damping cases
9. Time-domain oscillation analysis
10. Linear versus nonlinear comparison
11. Optional driven-pendulum analysis
12. Numerical-method verification
13. Limitations
14. Conclusions

### Acceptance criteria

The project is complete only if:

- All equilibria are correctly identified and classified.
- The Jacobian and eigenvalue analysis are correct.
- Phase portraits clearly distinguish oscillation, rotation, damping, and separatrices.
- Energy behavior agrees with the analytical derivation.
- The damping study shows the correct qualitative transition.
- The linear-versus-nonlinear comparison is quantitative.
- All plots are reproducible and properly labeled.
- The report explains both mathematical results and physical meaning.
