import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.state_space import StateSpaceModel
from src.transfer_function import calculate_tf_parameters
from src.integrators import explicit_euler, implicit_euler, rk4, scipy_solve, step_input
from src.metrics import calculate_rmse, calculate_mae
from src.dynamics import analytical_step_response, calculate_energy

def main():
    m, c, k = 2.0, 4.0, 20.0
    x0 = [0.0, 0.0]
    t_span = (0, 10)
    
    model = StateSpaceModel(m, c, k)
    tf_params = calculate_tf_parameters(m, c, k)
    print("Transfer Function Parameters:", tf_params)
    
    # 1. Reference Solution
    ref_sol = scipy_solve(model, t_span, x0, method="DOP853", rtol=1e-10, atol=1e-12, dense_output=True)
    t_ref = np.linspace(t_span[0], t_span[1], 1000)
    x_ref = ref_sol.sol(t_ref).T
    
    pd.DataFrame({'time': t_ref, 'x': x_ref[:,0], 'v': x_ref[:,1]}).to_csv('results/simulation_truth.csv', index=False)
    
    # 2. Plot Position and Velocity
    plt.figure()
    plt.plot(t_ref, x_ref[:,0], label="Position x(t)")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Position vs Time")
    plt.grid()
    plt.legend()
    plt.savefig("results/figures/position.png")
    
    plt.figure()
    plt.plot(t_ref, x_ref[:,1], label="Velocity v(t)", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs Time")
    plt.grid()
    plt.legend()
    plt.savefig("results/figures/velocity.png")
    
    # Phase Portrait
    plt.figure()
    plt.plot(x_ref[:,0], x_ref[:,1])
    plt.xlabel("Position (m)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Phase Portrait")
    plt.grid()
    plt.savefig("results/figures/phase_portrait.png")
    
    # Analytical vs Numerical
    t_eval = np.linspace(0, 10, 500)
    x_ana = analytical_step_response(t_eval, m, c, k)
    plt.figure()
    plt.plot(t_eval, x_ana, label="Analytical", linestyle='--')
    plt.plot(t_ref, x_ref[:,0], label="Numerical (DOP853)", alpha=0.5)
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Step Response Comparison")
    plt.legend()
    plt.grid()
    plt.savefig("results/figures/step_response.png")
    
    # 3. Integration Study
    step_sizes = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
    results = []
    
    for h in step_sizes:
        t_ee, x_ee = explicit_euler(model, t_span, x0, h)
        t_ie, x_ie = implicit_euler(model, t_span, x0, h)
        t_rk, x_rk = rk4(model, t_span, x0, h)
        
        for name, t_arr, x_arr in [("Euler", t_ee, x_ee), ("Implicit Euler", t_ie, x_ie), ("RK4", t_rk, x_rk)]:
            ref_vals = ref_sol.sol(t_arr).T
            rmse_val = calculate_rmse(x_arr[:,0], ref_vals[:,0])
            mae_val = calculate_mae(x_arr[:,0], ref_vals[:,0])
            results.append({"Method": name, "h": h, "RMSE": rmse_val, "MAE": mae_val})
            
    df_integ = pd.DataFrame(results)
    df_integ.to_csv("results/integration_comparison.csv", index=False)
    
    # Convergence Plot
    plt.figure()
    for method in ["Euler", "Implicit Euler", "RK4"]:
        subset = df_integ[df_integ["Method"] == method]
        plt.loglog(subset["h"], subset["RMSE"], marker='o', label=method)
    plt.xlabel("Step size h (s)")
    plt.ylabel("RMSE (m)")
    plt.title("Integration Convergence")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig("results/figures/convergence.png")
    
    # 4. Damping Study
    c_vals = [0, 4, 12, 20]
    damping_results = []
    plt.figure()
    for cv in c_vals:
        model_d = StateSpaceModel(m, cv, k)
        sol_d = scipy_solve(model_d, t_span, x0, method="RK45", max_step=0.01)
        plt.plot(sol_d.t, sol_d.y[0], label=f"c={cv}")
        damping_results.append({"c": cv, "max_overshoot": np.max(sol_d.y[0])})
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Damping Comparison")
    plt.legend()
    plt.grid()
    plt.savefig("results/figures/damping_comparison.png")
    pd.DataFrame(damping_results).to_csv("results/damping_study.csv", index=False)
    
    # 5. Energy Analysis (Undamped)
    model_u = StateSpaceModel(m, 0, k)
    t_ee, x_ee = explicit_euler(model_u, (0, 5), x0, 0.01) # no external force? wait, undamped case u(t)=0
    # Re-run with u(t)=0
    def explicit_euler_u0(model, t_span, x0, h):
        t = np.arange(t_span[0], t_span[1] + h, h)
        x = np.zeros((len(t), 2))
        x[0] = x0
        for i in range(len(t) - 1):
            x[i+1] = x[i] + h * model.state_derivative(x[i], 0.0).flatten()
        return t, x
    def implicit_euler_u0(model, t_span, x0, h):
        t = np.arange(t_span[0], t_span[1] + h, h)
        x = np.zeros((len(t), 2))
        x[0] = x0
        inv_mat = np.linalg.inv(np.eye(2) - h * model.A)
        for i in range(len(t) - 1):
            x[i+1] = inv_mat @ x[i]
        return t, x
    def rk4_u0(model, t_span, x0, h):
        t = np.arange(t_span[0], t_span[1] + h, h)
        x = np.zeros((len(t), 2))
        x[0] = x0
        for i in range(len(t) - 1):
            xi = x[i]
            k1 = model.state_derivative(xi, 0.0).flatten()
            k2 = model.state_derivative(xi + h/2 * k1, 0.0).flatten()
            k3 = model.state_derivative(xi + h/2 * k2, 0.0).flatten()
            k4 = model.state_derivative(xi + h * k3, 0.0).flatten()
            x[i+1] = xi + h/6 * (k1 + 2*k2 + 2*k3 + k4)
        return t, x

    # Initial condition x(0)=1 for undamped to have some energy
    x0_u = [1.0, 0.0] 
    t_ee_u, x_ee_u = explicit_euler_u0(model_u, (0, 10), x0_u, 0.01)
    t_ie_u, x_ie_u = implicit_euler_u0(model_u, (0, 10), x0_u, 0.01)
    t_rk_u, x_rk_u = rk4_u0(model_u, (0, 10), x0_u, 0.01)
    
    e_ee = calculate_energy(x_ee_u[:,0], x_ee_u[:,1], m, k)
    e_ie = calculate_energy(x_ie_u[:,0], x_ie_u[:,1], m, k)
    e_rk = calculate_energy(x_rk_u[:,0], x_rk_u[:,1], m, k)
    e_exact = calculate_energy(np.cos(np.sqrt(k/m)*t_ee_u), -np.sqrt(k/m)*np.sin(np.sqrt(k/m)*t_ee_u), m, k)
    
    plt.figure()
    plt.plot(t_ee_u, e_exact, label="Exact")
    plt.plot(t_ee_u, e_ee, label="Explicit Euler")
    plt.plot(t_ie_u, e_ie, label="Implicit Euler")
    plt.plot(t_rk_u, e_rk, label="RK4")
    plt.xlabel("Time (s)")
    plt.ylabel("Energy (J)")
    plt.title("Energy Conservation")
    plt.legend()
    plt.grid()
    plt.savefig("results/figures/energy.png")

if __name__ == "__main__":
    main()
