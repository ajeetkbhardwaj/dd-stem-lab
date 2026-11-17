import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.pendulum import PendulumSimulator
from src.integrators import integrator_convergence_study, plot_convergence
from src.analysis import sampling_study
from src.measurement import generate_measurements

def main():
    # Setup directories
    os.makedirs('results/figures', exist_ok=True)
    
    # 1. Truth Simulation
    sim = PendulumSimulator(m=1.0, L=1.0, g=9.81, b=0.1)
    t_span = (0.0, 10.0)
    y0 = [1.2, 0.0]
    
    print("Running truth simulation...")
    t_truth, y_truth = sim.simulate(t_span, y0, method="DOP853", rtol=1e-12, atol=1e-14)
    theta_truth = y_truth[:, 0]
    omega_truth = y_truth[:, 1]
    
    truth_df = pd.DataFrame({'time': t_truth, 'theta': theta_truth, 'omega': omega_truth})
    truth_df.to_csv('results/truth_simulation.csv', index=False)
    
    # Plot truth
    plt.figure(figsize=(10, 5))
    plt.plot(t_truth, theta_truth, label='$\\theta(t)$')
    plt.plot(t_truth, omega_truth, label='$\\dot{\\theta}(t)$')
    plt.xlabel('Time [s]')
    plt.ylabel('State')
    plt.title('Truth Simulation')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/figures/truth_simulation.png')
    plt.close()

    # 2. Measurement Model & Sampling Study
    print("Running sampling study...")
    sampling_periods = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
    df_sampling = sampling_study(t_truth, theta_truth, omega_truth, sampling_periods, save_dir='results/figures')
    df_sampling.to_csv('results/sampling_study.csv', index=False)
    print(df_sampling)
    
    # 3. Integrator Convergence Study
    print("Running integrator study...")
    step_sizes = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
    df_integrator = integrator_convergence_study(sim, t_span, y0, step_sizes=step_sizes)
    df_integrator.to_csv('results/integrator_study.csv', index=False)
    plot_convergence(df_integrator, save_path='results/figures/integrator_convergence.png')

    # 4. Energy Analysis (Undamped)
    print("Running energy analysis...")
    sim_undamped = PendulumSimulator(m=1.0, L=1.0, g=9.81, b=0.0)
    t_span_energy = (0, 5)
    dt_energy = 0.05
    
    # Exact/Reference
    t_ref, y_ref = sim_undamped.simulate(t_span_energy, y0, method="DOP853")
    E_ref = sim_undamped.energy(y_ref)
    
    # Euler
    t_eu, y_eu = sim_undamped.simulate(t_span_energy, y0, method="euler", dt=dt_energy)
    E_eu = sim_undamped.energy(y_eu)
    
    # RK4
    t_rk, y_rk = sim_undamped.simulate(t_span_energy, y0, method="rk4", dt=dt_energy)
    E_rk = sim_undamped.energy(y_rk)
    
    plt.figure(figsize=(10, 5))
    plt.plot(t_ref, E_ref, label='Reference (DOP853)')
    plt.plot(t_eu, E_eu, label='Euler')
    plt.plot(t_rk, E_rk, label='RK4')
    plt.xlabel('Time [s]')
    plt.ylabel('Energy [J]')
    plt.title('Energy Conservation (Undamped Pendulum)')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/figures/energy_analysis.png')
    plt.close()
    print("Done!")

if __name__ == "__main__":
    main()
