import numpy as np
import pandas as pd
from src.pendulum_dynamics import NonlinearPendulum
from src.equilibrium_analysis import analyze_equilibria
from src.phase_portrait import generate_phase_portrait
from src.energy_analysis import analyze_energy
from src.linear_vs_nonlinear import compare_linear_nonlinear

def main():
    m, L, g = 1.0, 1.0, 9.81
    damping_values = [0.0, 0.1, 0.5, 1.0, 2.0, 5.0]
    
    initial_conditions = [
        (0.1, 0), (1.0, 0), (2.0, 0), (3.0, 0),
        (0, 2), (0, 5), (0, 8),
        (np.pi-0.1, 0), (np.pi+0.1, 0)
    ]
    
    all_equilibria = []
    
    for b in damping_values:
        print(f"Processing b={b}...")
        pendulum = NonlinearPendulum(m, L, g, b)
        
        # 1. Equilibria Analysis
        eqs = analyze_equilibria(pendulum)
        for eq in eqs:
            eq["b"] = b
            all_equilibria.append(eq)
            
        # 2. Phase Portraits
        generate_phase_portrait(pendulum, initial_conditions, t_span=(0, 20), filename=f"results/figures/phase_portrait_b_{b}.png")
        
        # 3. Energy Analysis
        analyze_energy(pendulum, initial_condition=(1.5, 0), t_span=(0, 20), filename=f"results/figures/energy_b_{b}.png")
        
    df_eq = pd.DataFrame(all_equilibria)
    df_eq.to_csv("results/equilibria.csv", index=False)
    
    # 4. Linear vs Nonlinear Comparison
    print("Comparing Linear vs Nonlinear...")
    initial_angles = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    df_ln = compare_linear_nonlinear(initial_angles, filename="results/figures/linear_vs_nonlinear_rmse.png")
    df_ln.to_csv("results/linear_vs_nonlinear.csv", index=False)
    print("Done!")

if __name__ == "__main__":
    main()
