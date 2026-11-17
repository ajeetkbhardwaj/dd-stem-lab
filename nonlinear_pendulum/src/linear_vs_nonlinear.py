import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from src.pendulum_dynamics import NonlinearPendulum, LinearPendulum

def compare_linear_nonlinear(initial_angles, t_span=(0, 10), filename=None):
    m, L, g = 1.0, 1.0, 9.81
    
    nonlinear = NonlinearPendulum(m, L, g, 0.0)
    linear = LinearPendulum(m, L, g, 0.0)
    
    results = []
    
    for theta_0 in initial_angles:
        ic = [theta_0, 0.0]
        
        sol_non = solve_ivp(nonlinear.rhs, t_span, ic, max_step=0.05, dense_output=True)
        sol_lin = solve_ivp(linear.rhs, t_span, ic, max_step=0.05, dense_output=True)
        
        t_eval = np.linspace(t_span[0], t_span[1], 500)
        theta_non = sol_non.sol(t_eval)[0]
        theta_lin = sol_lin.sol(t_eval)[0]
        
        rmse = np.sqrt(np.mean((theta_non - theta_lin)**2))
        results.append({"theta_0": theta_0, "RMSE": rmse})
        
    df = pd.DataFrame(results)
    
    plt.figure()
    plt.plot(df['theta_0'], df['RMSE'], marker='o')
    plt.xlabel('Initial Angle (rad)')
    plt.ylabel('RMSE (rad)')
    plt.title('Linear vs Nonlinear Pendulum RMSE')
    plt.grid(True)
    if filename:
        plt.savefig(filename)
    plt.close()
    
    return df
