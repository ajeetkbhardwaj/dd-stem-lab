import numpy as np
from scipy.integrate import solve_ivp

def step_input(t):
    return 10.0 if t >= 0 else 0.0

def explicit_euler(model, t_span, x0, h):
    t = np.arange(t_span[0], t_span[1] + h, h)
    x = np.zeros((len(t), 2))
    x[0] = x0
    for i in range(len(t) - 1):
        u = step_input(t[i])
        x[i+1] = x[i] + h * model.state_derivative(x[i], u).flatten()
    return t, x

def implicit_euler(model, t_span, x0, h):
    t = np.arange(t_span[0], t_span[1] + h, h)
    x = np.zeros((len(t), 2))
    x[0] = x0
    I = np.eye(2)
    # (I - hA) x_{k+1} = x_k + h B u_{k+1}
    inv_mat = np.linalg.inv(I - h * model.A)
    for i in range(len(t) - 1):
        u = step_input(t[i+1])
        rhs = x[i] + h * (model.B @ np.array([u])).flatten()
        x[i+1] = inv_mat @ rhs
    return t, x

def rk4(model, t_span, x0, h):
    t = np.arange(t_span[0], t_span[1] + h, h)
    x = np.zeros((len(t), 2))
    x[0] = x0
    for i in range(len(t) - 1):
        ti = t[i]
        xi = x[i]
        k1 = model.state_derivative(xi, step_input(ti)).flatten()
        k2 = model.state_derivative(xi + h/2 * k1, step_input(ti + h/2)).flatten()
        k3 = model.state_derivative(xi + h/2 * k2, step_input(ti + h/2)).flatten()
        k4 = model.state_derivative(xi + h * k3, step_input(ti + h)).flatten()
        x[i+1] = xi + h/6 * (k1 + 2*k2 + 2*k3 + k4)
    return t, x

def scipy_solve(model, t_span, x0, method, **kwargs):
    def f(t, y):
        return model.state_derivative(y, step_input(t)).flatten()
    sol = solve_ivp(f, t_span, x0, method=method, **kwargs)
    return sol
