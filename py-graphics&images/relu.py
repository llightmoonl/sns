import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

x = np.linspace(-10, 10, 100)
y = np.maximum(x, 0)
n_steps = len(x)

fig, ax = plt.subplots(figsize=(9, 6))
ax.set_xlim(x.min(), x.max())
ax.set_ylim(-1, 11)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("График функции ReLU")
ax.grid(True, linestyle="--", alpha=0.5)

line_pos, = ax.plot([], [], color="teal", linewidth=2, label="ReLU (x > 0)")
line_neg, = ax.plot([], [], color="crimson", linewidth=2, label="ReLU (x ≤ 0)")

current_fill_pos = None
current_fill_neg = None

def init():
    line_pos.set_data([], [])
    line_neg.set_data([], [])
    return line_pos, line_neg

def update(frame):
    current_x = x[:frame+1]
    current_y = y[:frame+1]
    mask_pos = current_x > 0
    mask_neg = ~mask_pos
    if mask_pos.any():
        line_pos.set_data(current_x[mask_pos], current_y[mask_pos])
        line_neg.set_data(current_x[mask_neg], current_y[mask_neg])
    else:
        line_pos.set_data([], [])
        line_neg.set_data(current_x, current_y)
    global current_fill_pos, current_fill_neg
    if current_fill_pos:
        current_fill_pos.remove()
    if current_fill_neg:
        current_fill_neg.remove()
    if mask_pos.any():
        current_fill_pos = ax.fill_between(current_x[mask_pos], current_y[mask_pos], color="teal", alpha=0.2)
    if mask_neg.any():
        current_fill_neg = ax.fill_between(current_x[mask_neg], current_y[mask_neg], color="crimson", alpha=0.2)
    new_width = 1 + frame / n_steps * 2
    line_pos.set_linewidth(new_width)
    line_neg.set_linewidth(new_width)    
    ax.set_title(f"График функции ReLU: {frame+1}/{n_steps}")
    artists = [line_pos, line_neg]    
    if current_fill_pos:
        artists.extend(current_fill_pos.get_children())
    if current_fill_neg:
        artists.extend(current_fill_neg.get_children())        
    return artists

ani = FuncAnimation(
    fig,
    update,
    frames=n_steps,
    init_func=init,
    interval=20,
    blit=True,
    repeat=False
)

writer = PillowWriter(fps=30)
ani.save("relu.gif", writer=writer)
plt.close()