import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def calculate_energy(pendulum, theta, omega):
    KE = 0.5 * pendulum.m * pendulum.L**2 * omega**2
    PE = pendulum.m * pendulum.g * pendulum.L * (1 - np.cos(theta))
    return KE + PE

def analyze_energy(pendulum, initial_condition=(1.5, 0), t_span=(0, 20), filename=None):
    sol = solve_ivp(pendulum.rhs, t_span, initial_condition, max_step=0.01)
    t = sol.t
    theta = sol.y[0]
    omega = sol.y[1]
    
    E = calculate_energy(pendulum, theta, omega)
    
    plt.figure()
    plt.plot(t, E, label=f'Energy (b={pendulum.b})')
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.title('Energy vs Time')
    plt.grid(True)
    plt.legend()
    if filename:
        plt.savefig(filename)
    plt.close()
    
    return t, E
