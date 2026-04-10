import numpy as np
import matplotlib.pyplot as plt
import imageio

H, W = 3, 3
D = H * W  # 9

flat_vals = np.arange(1, D + 1)
np.random.shuffle(flat_vals)

np.random.seed(42)
colors = plt.cm.tab10(np.linspace(0, 1, D))

fig = plt.figure(figsize=(8, 4))
fig.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.85, wspace=0.3)

ax_left = fig.add_subplot(121)
ax_right = fig.add_subplot(122)

title_left = ax_left.set_title("Многомерный массив", fontsize=16, pad=20)
title_left.set_y(1.05)

title_right = ax_right.set_title("Одномерный массив", fontsize=16, pad=20)
title_right.set_y(1.05)

for ax in (ax_left, ax_right):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

left_texts = [[None for _ in range(W)] for _ in range(H)]
left_rects = [[None for _ in range(W)] for _ in range(H)]
right_texts = [None for _ in range(D)]
right_rects = [None for _ in range(D)]

left_matrix_values = flat_vals.reshape(H, W)

for i in range(H):
    for j in range(W):
        val = left_matrix_values[i, j]
        color_idx = np.where(flat_vals == val)[0][0]
        color = colors[color_idx]        
        rect = plt.Rectangle((j, H-1-i), 1, 1, edgecolor="k", facecolor=color, lw=1)
        ax_left.add_patch(rect)
        left_rects[i][j] = rect        
        left_texts[i][j] = ax_left.text(j+0.5, H-0.5-i, str(val),
                   ha="center", va="center", fontsize=20, fontweight="bold", color="white")

ax_left.set_xlim(0, W)
ax_left.set_ylim(0, H)
ax_left.set_aspect("equal")

for k in range(D):
    rect = plt.Rectangle((0, D-1-k), 0.4, 1, edgecolor="k", facecolor="white", lw=1)
    ax_right.add_patch(rect)
    right_rects[k] = rect
    right_texts[k] = ax_right.text(0.2, D-0.5-k, "", ha="center", va="center",
               fontsize=16, fontweight="bold", color="black")

ax_right.set_xlim(0, 0.4)
ax_right.set_ylim(0, D)
ax_right.set_aspect("auto")

frames = []

def init():
    for k in range(D):
        right_texts[k].set_text("")
        right_rects[k].set_facecolor("white")
    return (*right_texts, *right_rects)

def animate(n):
    i = n // W
    j = n % W
    val = flat_vals[n]
    color_idx = n
    color = colors[color_idx]    
    rect_highlight = plt.Rectangle((j, H-1-i), 1, 1,
                                   edgecolor="red", facecolor="none", lw=3, linestyle="--")
    ax_left.add_patch(rect_highlight)    
    right_texts[n].set_text(str(val))
    right_rects[n].set_facecolor(color)
    right_texts[n].set_color("white")    
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)    
    [p.remove() for p in ax_left.patches if p.get_edgecolor() == (1.0, 0.0, 0.0, 1.0)]    
    return (*right_texts, *right_rects)

for n in range(D):
    animate(n)
imageio.mimsave("flatten.gif", frames, duration=2000, loop=0)
plt.close(fig)