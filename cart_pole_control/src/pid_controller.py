import numpy as np

class PIDController:
    """PID on pendulum angle only."""
    def __init__(self, Kp=50.0, Ki=5.0, Kd=10.0, u_max=20.0, Ts=0.02):
        self.Kp   = Kp
        self.Ki   = Ki
        self.Kd   = Kd
        self.u_max = u_max
        self.Ts   = Ts
        self._integral = 0.0
        self._prev_err = 0.0

    def reset(self):
        self._integral = 0.0
        self._prev_err = 0.0

    def compute(self, theta):
        err            = -theta          # reference = 0
        self._integral += err * self.Ts
        derivative     = (err - self._prev_err) / self.Ts
        self._prev_err = err

        u = self.Kp * err + self.Ki * self._integral + self.Kd * derivative
        return float(np.clip(u, -self.u_max, self.u_max))
