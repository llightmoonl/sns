import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio

H_in, W_in = 9, 9
kernel_size = 3
stride = 1

H_out = (H_in - kernel_size) // stride + 1
W_out = (H_in - kernel_size) // stride + 1

np.random.seed(42)
input_matrix = np.random.randint(0, 10, size=(H_in, W_in))

kernel = np.array([
    [1, 0, -1],
    [1, 0, -1],
    [1, 0, -1]
])

fig = plt.figure(figsize=(16, 9))
fig.subplots_adjust(left=0.05, right=0.95, bottom=0.25, top=0.85, wspace=0.4, hspace=0.3)

ax_left = fig.add_subplot(131)
ax_kernel = fig.add_subplot(132)
ax_right = fig.add_subplot(133)

for ax in (ax_left, ax_kernel, ax_right):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

ax_left.set_title("Входная карта (input)", fontsize=16, pad=20)
ax_kernel.set_title("Ядро свертки (kernel)", fontsize=16, pad=20)
ax_right.set_title("Выходная карта (output)", fontsize=16, pad=20)

cell_size = 1.5

num_blocks = H_out * W_out
unique_colors = plt.cm.hsv(np.linspace(0, 0.8, num_blocks))
block_colors = [tuple(color) for color in unique_colors]

left_rects = [[None for _ in range(W_in)] for _ in range(H_in)]
left_texts = [[None for _ in range(W_in)] for _ in range(H_in)]

for i in range(H_in):
    for j in range(W_in):
        rect = plt.Rectangle((j * cell_size, (H_in-1-i) * cell_size), cell_size, cell_size,
                             edgecolor="black", facecolor="white", lw=2)
        ax_left.add_patch(rect)
        left_rects[i][j] = rect        
        left_texts[i][j] = ax_left.text(j * cell_size + cell_size/2, (H_in-0.5-i) * cell_size, str(input_matrix[i, j]),
                           ha="center", va="center", fontsize=12, fontweight="bold", color="black")

ax_left.set_xlim(0, W_in * cell_size)
ax_left.set_ylim(0, H_in * cell_size)
ax_left.set_aspect("equal")

for i in range(kernel_size):
    for j in range(kernel_size):
        rect = plt.Rectangle((j * cell_size, (kernel_size-1-i) * cell_size), cell_size, cell_size,
                             edgecolor="black", facecolor="white", lw=2)
        ax_kernel.add_patch(rect)        
        ax_kernel.text(j * cell_size + cell_size/2, (kernel_size-0.5-i) * cell_size, str(kernel[i, j]),
                       ha="center", va="center", fontsize=20, fontweight="bold", color="black")

ax_kernel.set_xlim(0, kernel_size * cell_size)
ax_kernel.set_ylim(0, kernel_size * cell_size)
ax_kernel.set_aspect("equal")

right_rects = [[None for _ in range(W_out)] for _ in range(H_out)]
right_texts = [[None for _ in range(W_out)] for _ in range(H_out)]

for i in range(H_out):
    for j in range(W_out):
        rect = plt.Rectangle((j * cell_size, (H_out-1-i) * cell_size), cell_size, cell_size, edgecolor="k", facecolor="white", lw=2)
        ax_right.add_patch(rect)
        right_rects[i][j] = rect
        right_texts[i][j] = ax_right.text(j * cell_size + cell_size/2, (H_out-0.5-i) * cell_size, "",
                            ha="center", va="center", fontsize=14, fontweight="bold", color="black")

ax_right.set_xlim(0, W_out * cell_size)
ax_right.set_ylim(0, H_out * cell_size)
ax_right.set_aspect("equal")

calc_text = fig.text(0.5, 0.15, "", ha="center", va="center",
                 fontsize=14, fontweight="bold", transform=fig.transFigure)

frames = []
D_out = H_out * W_out

def init():
    for i in range(H_in):
        for j in range(W_in):
            left_rects[i][j].set_facecolor("lightgrey")
            left_texts[i][j].set_color("white")
    calc_text.set_text("")
    return (*[t for row in left_texts for t in row], *[t for row in right_texts for t in row],
            *[r for row in left_rects for r in row], *[r for row in right_rects for r in row], calc_text)

def animate(frame):
    window_row = frame // W_out
    window_col = frame % W_out
    i_start_anim = window_row * stride
    j_start_anim = window_col * stride
    rect_highlight_window = plt.Rectangle((j_start_anim * cell_size, (H_in-1-i_start_anim - 2) * cell_size),
                                   kernel_size * cell_size, kernel_size * cell_size,
                                   edgecolor="black", facecolor="none", lw=6)
    ax_left.add_patch(rect_highlight_window)
    window_data = input_matrix[i_start_anim:i_start_anim+kernel_size, j_start_anim:j_start_anim+kernel_size]
    conv_val = np.sum(window_data * kernel)
    block_color = block_colors[frame]    
    for i_offset in range(kernel_size):
        for j_offset in range(kernel_size):
            i_cell = i_start_anim + i_offset
            j_cell = j_start_anim + j_offset
            left_rects[i_cell][j_cell].set_facecolor(block_color)    
    right_texts[window_row][window_col].set_text(str(int(conv_val)))
    right_rects[window_row][window_col].set_facecolor(block_color)
    calc_parts = []
    total_sum = 0
    for i in range(kernel_size):
        for j in range(kernel_size):
            input_val = window_data[i, j]
            kernel_val = kernel[i, j]
            product = input_val * kernel_val
            total_sum += product
            if product != 0:
                calc_parts.append(f"{input_val}×{kernel_val}")
    formula_part = " + ".join(calc_parts)
    solution_part = f" = {total_sum}"
    full_calc_str = f"{formula_part}{solution_part}"
    general_formula = r"$\sum_{i=0}^{2} \, \sum_{j=0}^{2} \text{input}[i,j] \times \text{kernel}[i,j]$"
    combined_calc = f"{general_formula} \n {full_calc_str}"
    step_info = f"Шаг {frame + 1}/{D_out}: "
    display_text = step_info + combined_calc
    calc_text.set_text(display_text)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)
    [p.remove() for p in ax_left.patches if p.get_linewidth() == 6]
    return (*[t for row in left_texts for t in row], *[t for row in right_texts for t in row],
            *[r for row in left_rects for r in row], *[r for row in right_rects for r in row], calc_text)

ani = []
for frame in range(D_out):
    ani.append(animate(frame))
iio.imwrite("conv2d.gif", frames, duration=5000, loop=0)
plt.close(fig)