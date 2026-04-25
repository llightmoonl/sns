import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, FancyArrowPatch

input_size = 10
hidden_size = 5
output_size = 3

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

np.random.seed(42)
input_vector = np.random.randn(input_size) * 0.5

w1 = np.random.randn(hidden_size, input_size) * np.sqrt(2.0 / input_size)
b1 = np.zeros(hidden_size)

hidden_pre_activation = np.dot(w1, input_vector) + b1
hidden_vector = sigmoid(hidden_pre_activation)

w2 = np.random.randn(output_size, hidden_size) * np.sqrt(2.0 / hidden_size)
b2 = np.zeros(output_size)

output_pre_activation = np.dot(w2, hidden_vector) + b2
output_vector = sigmoid(output_pre_activation)

fig, ax = plt.subplots(figsize=(16, 10))

layer_distance = 8.0
neuron_spacing = 2.0
neuron_radius = 0.6
text_offset_y = 2.5

input_positions = [(0, i * neuron_spacing - (input_size - 1) * neuron_spacing / 2) for i in range(input_size)]
hidden_positions = [(layer_distance, i * neuron_spacing - (hidden_size - 1) * neuron_spacing / 2) for i in range(hidden_size)]
output_positions = [(2 * layer_distance, i * neuron_spacing - (output_size - 1) * neuron_spacing / 2) for i in range(output_size)]

max_y_pos = max(
    max([pos[1] for pos in input_positions]),
    max([pos[1] for pos in hidden_positions]),
    max([pos[1] for pos in output_positions])
)

min_y_pos = min(
    min([pos[1] for pos in input_positions]),
    min([pos[1] for pos in hidden_positions]),
    min([pos[1] for pos in output_positions])
)

ax.set_xlim(-1, 2 * layer_distance + 1)
ax.set_ylim(min_y_pos - neuron_radius - 1, max_y_pos + neuron_radius + text_offset_y)
ax.set_aspect("equal")
ax.axis("off")

def draw_neuron(x, y, value, is_active=False, size=neuron_radius):
    color = "orange" if is_active else "lightblue"
    alpha = 1.0 if is_active else 0.7
    circle = Circle((x, y), size, color=color, ec="black", lw=1.5, alpha=alpha)
    ax.add_patch(circle)
    ax.text(x, y, f"{value:.2f}", ha="center", va="center", fontsize=8, color="black")

def draw_arrow(x1, y1, x2, y2, weight, is_active=False):
    color = "red" if is_active else "gray"
    alpha = 1.0 if is_active else 0.3
    linewidth = 2.0 if is_active else 0.5
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        mutation_scale=8,
        shrinkA=1,
        shrinkB=1,
        connectionstyle="arc3,rad=-0.1",
        color=color,
        alpha=alpha,
        linewidth=linewidth
    )
    ax.add_artist(arrow)

def draw_connections(active_input_idx=None, active_hidden_idx=None):
    for i, (xi, yi) in enumerate(input_positions):
        for j, (xh, yh) in enumerate(hidden_positions):
            weight = w1[j, i]
            is_active = (active_input_idx == i)
            draw_arrow(xi, yi, xh, yh, weight, is_active)
    for j, (xh, yh) in enumerate(hidden_positions):
        for k, (xo, yo) in enumerate(output_positions):
            weight = w2[k, j]
            is_active = (active_hidden_idx == j)
            draw_arrow(xh, yh, xo, yo, weight, is_active)

def update(frame):
    ax.clear()
    ax.set_xlim(-1, 2 * layer_distance + 1)
    ax.set_ylim(min_y_pos - neuron_radius - 1, max_y_pos + neuron_radius + text_offset_y)
    ax.axis("off")
    total_stages = 3
    stage = frame % total_stages
    neuron_idx = (input_size - 1) - ((frame // total_stages) % input_size)
    active_input = None
    active_hidden = None
    if stage == 0:
        active_input = neuron_idx
        stage_text = f"Этап 1: Сигнал от входного нейрона"
    elif stage == 1:
        active_input = neuron_idx
        active_hidden = (hidden_size - 1) - (neuron_idx % hidden_size)
        stage_text = f"Этап 2: Активация скрытого нейрона"
    else:
        active_input = neuron_idx
        active_hidden = (hidden_size - 1) - (neuron_idx % hidden_size)
        stage_text = "Этап 3: Активация выходного слоя"
    draw_connections(active_input, active_hidden)
    for i, (xi, yi) in enumerate(input_positions):
        is_active = (i == neuron_idx and stage >= 0)
        draw_neuron(xi, yi, input_vector[i], is_active)
    for j, (xh, yh) in enumerate(hidden_positions):
        is_active = (j == active_hidden and stage >= 1)
        draw_neuron(xh, yh, hidden_vector[j], is_active)
    for k, (xo, yo) in enumerate(output_positions):
        is_active = (stage == 2) 
        draw_neuron(xo, yo, output_vector[k], is_active)
    ax.text(-0.5, max_y_pos + 1.5,
            "Входной слой", ha="center", va="bottom", fontsize=14)
    ax.text(layer_distance, max_y_pos + 1.5,
            "Слой Dense", ha="center", va="bottom", fontsize=14)
    ax.text(2 * layer_distance + 0.5, max_y_pos + 1.5,
            "Выходной слой", ha="center", va="bottom", fontsize=14)
    ax.text(layer_distance, min_y_pos - 2,
            stage_text, ha="center", va="bottom", fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))

total_frames = input_size * 3
ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=2500, repeat=False)
ani.save("dense.gif", writer="pillow", fps=0.5, dpi=100)
plt.close(fig)