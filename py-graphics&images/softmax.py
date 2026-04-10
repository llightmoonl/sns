import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

x = np.linspace(-5, 5, 100)

fig, ax = plt.subplots(figsize=(9, 6))
ax.set_xlim(x.min(), x.max())
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("График функции Softmax")
ax.grid(True, linestyle="--", alpha=0.5)

line_softmax, = ax.plot([], [], color="teal", linewidth=2, label="Softmax")

current_fill = None
tau_values = np.linspace(1.0, 0.1, 200)

def softmax(x, tau=1.0):
    return 1 / (1 + np.exp(-x / tau))

def init():
    line_softmax.set_data([], [])
    return line_softmax,

def update(frame):
    global current_fill
    if frame < len(x):
        current_x = x[:frame+1]
        tau = tau_values[0]
        current_y = softmax(current_x, tau)        
        line_softmax.set_data(current_x, current_y)
        ax.set_title(f"График функции Softmax (параметр τ={tau:.2f})")        
        if current_fill:
            current_fill.remove()
        if len(current_x) > 0:
            current_fill = ax.fill_between(current_x, current_y, color="teal", alpha=0.2)        
        line_softmax.set_linewidth(1 + frame / len(x) * 2)        
        artists = [line_softmax]
        if current_fill:
            artists.extend(current_fill.get_children())
        return artists
    else:
        line_softmax.set_data(x, softmax(x, tau=tau_values[0]))        
        tau_idx = frame - len(x)
        if tau_idx >= len(tau_values):
            tau_idx = len(tau_values) - 1            
        tau = tau_values[tau_idx]
        y_new = softmax(x, tau)        
        line_softmax.set_ydata(y_new)
        ax.set_title(f"Влияние параметра τ на график функции Softmax (τ={tau:.3f})")        
        if current_fill:
            current_fill.remove()
        current_fill = ax.fill_between(x, y_new, color="teal", alpha=0.2)        
        artists = [line_softmax]
        artists.extend(current_fill.get_children())
        return artists

total_frames = len(x) + len(tau_values)

ani = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    init_func=init,
    interval=25,
    blit=True,
    repeat=False
)

writer = PillowWriter(fps=30)
ani.save("softmax.gif", writer=writer)
plt.close()