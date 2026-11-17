import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def generate_phase_portrait(pendulum, initial_conditions, t_span=(0, 20), filename=None):
    plt.figure(figsize=(10, 6))
    
    # Vector field
    theta_vals = np.linspace(-3*np.pi, 3*np.pi, 30)
    omega_vals = np.linspace(-10, 10, 30)
    Theta, Omega = np.meshgrid(theta_vals, omega_vals)
    U = Omega
    V = - (pendulum.g / pendulum.L) * np.sin(Theta) - (pendulum.b / (pendulum.m * pendulum.L**2)) * Omega
    plt.streamplot(Theta, Omega, U, V, color='lightgray', density=1.5)
    
    # Plot trajectories
    for ic in initial_conditions:
        sol = solve_ivp(pendulum.rhs, t_span, ic, max_step=0.05)
        plt.plot(sol.y[0], sol.y[1], linewidth=1.5)
        
    plt.title(f"Phase Portrait (b={pendulum.b})")
    plt.xlabel(r"$\theta$ (rad)")
    plt.ylabel(r"$\dot{\theta}$ (rad/s)")
    plt.xlim(-3*np.pi, 3*np.pi)
    plt.ylim(-10, 10)
    plt.grid(True)
    if filename:
        plt.savefig(filename)
    plt.close()
