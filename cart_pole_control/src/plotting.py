import matplotlib.pyplot as plt
import numpy as np

def plot_response(t, states, forces, title, filepath):
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))

    axes[0].plot(t, states[:, 0], label='Cart position x (m)')
    axes[0].set_ylabel('Position (m)'); axes[0].legend(); axes[0].grid()
    axes[0].set_title(title)

    axes[1].plot(t, np.degrees(states[:, 2]), label='Angle θ (deg)', color='tab:orange')
    axes[1].axhline(0, color='k', lw=0.8)
    axes[1].set_ylabel('Angle (deg)'); axes[1].legend(); axes[1].grid()

    axes[2].step(t, forces, where='post', color='tab:red', label='Control force u (N)')
    axes[2].axhline(20,  color='k', lw=0.8, ls='--')
    axes[2].axhline(-20, color='k', lw=0.8, ls='--')
    axes[2].set_xlabel('Time (s)'); axes[2].set_ylabel('Force (N)')
    axes[2].legend(); axes[2].grid()

    plt.tight_layout()
    plt.savefig(filepath, dpi=100)
    plt.close()

def plot_phase(t, states, title, filepath):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(states[:, 2], states[:, 3])
    axes[0].set_xlabel('θ (rad)'); axes[0].set_ylabel('θ̇ (rad/s)')
    axes[0].set_title(f'{title} - θ phase')
    axes[0].grid()

    axes[1].plot(states[:, 0], states[:, 1])
    axes[1].set_xlabel('x (m)'); axes[1].set_ylabel('ẋ (m/s)')
    axes[1].set_title(f'{title} - x phase')
    axes[1].grid()

    plt.tight_layout()
    plt.savefig(filepath, dpi=100)
    plt.close()

def plot_comparison(results_dict, metric_key, ylabel, title, filepath):
    names = list(results_dict.keys())
    vals  = [results_dict[n][metric_key] for n in names]
    plt.figure(figsize=(8, 5))
    bars = plt.bar(names, vals, color=['#4c72b0','#dd8452','#55a868'])
    plt.ylabel(ylabel); plt.title(title); plt.grid(axis='y')
    for bar, v in zip(bars, vals):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*max(vals),
                 f'{v:.3f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(filepath, dpi=100)
    plt.close()
