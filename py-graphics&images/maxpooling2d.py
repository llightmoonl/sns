import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio

H_in, W_in = 4, 4
H_out, W_out = 2, 2
kernel_size = 2
stride = 2

np.random.seed(42)
input_matrix = np.array([
    [10, 5, 14, 26],
    [6, 16, 20, 8],
    [30, 7, 9, 17],
    [13, 22, 27, 11]
])

block_cmaps = [
    plt.cm.Blues,
    plt.cm.Greens,
    plt.cm.Purples,
    plt.cm.Oranges
]
block_edge_colors = ["darkblue", "darkgreen", "darkviolet", "darkorange"]

fig = plt.figure(figsize=(10, 5))
fig.subplots_adjust(left=0.1, right=0.9, bottom=0.15, top=0.85)
ax_left = fig.add_subplot(121)
ax_right = fig.add_subplot(122)

for ax in (ax_left, ax_right):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

left_rects = [[None for _ in range(W_in)] for _ in range(H_in)]
left_texts = [[None for _ in range(W_in)] for _ in range(H_in)]
block_norms = []

for br in range(H_out):
    for bc in range(W_out):
        i_start, j_start = br*stride, bc*stride
        block = input_matrix[i_start:i_start+kernel_size, j_start:j_start+kernel_size]
        block_norms.append(plt.Normalize(vmin=block.min() * 0.01, vmax=block.max()))

for i in range(H_in):
    for j in range(W_in):
        block_row = i // kernel_size
        block_col = j // kernel_size
        block_idx = block_row * W_out + block_col
        norm = block_norms[block_idx]
        cmap = block_cmaps[block_idx]
        face_color = cmap(norm(input_matrix[i, j]))
        rect = plt.Rectangle((j, H_in-1-i), 1, 1,
                             edgecolor="none", facecolor=face_color, lw=0)
        ax_left.add_patch(rect)
        left_rects[i][j] = rect

for br in range(H_out):
    for bc in range(W_out):
        block_idx = br * W_out + bc
        edge_color = block_edge_colors[block_idx]        
        i_start_anim = br * stride + 1
        j_start_anim = bc * stride
        rect_block_frame = plt.Rectangle((j_start_anim, H_in-1-i_start_anim),
                                         kernel_size, kernel_size,
                                         edgecolor=edge_color, facecolor='none', lw=4)
        ax_left.add_patch(rect_block_frame)

for i in range(H_in):
    for j in range(W_in):
        left_texts[i][j] = ax_left.text(j+0.5, H_in-0.5-i, str(input_matrix[i, j]),
                           ha="center", va="center", fontsize=22, fontweight="bold", color="white")

ax_left.set_xlim(0, W_in)
ax_left.set_ylim(0, H_in)
ax_left.set_aspect("equal")
ax_left.set_title("Входная карта", fontsize=16, pad=20)

right_texts = [[None for _ in range(W_out)] for _ in range(H_out)]
right_rects = [[None for _ in range(W_out)] for _ in range(H_out)]

for i in range(H_out):
    for j in range(W_out):
        rect = plt.Rectangle((j, H_out-1-i), 1, 1, edgecolor="k", facecolor="white", lw=2)
        ax_right.add_patch(rect)
        right_rects[i][j] = rect
        right_texts[i][j] = ax_right.text(j+0.5, H_out-0.5-i, "",
                            ha="center", va="center", fontsize=26, fontweight="bold", color="black")

ax_right.set_xlim(0, W_out)
ax_right.set_ylim(0, H_out)
ax_right.set_aspect("equal")
ax_right.set_title("Выходная карта", fontsize=16, pad=20)


frames = []

def animate(frame):
    window_row = frame // W_out
    window_col = frame % W_out
    i_start_anim = window_row * stride + 1 
    j_start_anim = window_col * stride
    i_start_calc = window_row * stride 
    j_start_calc = window_col * stride
    rect_highlight_window = plt.Rectangle((j_start_anim, H_in-1-i_start_anim),
                                   kernel_size, kernel_size,
                                   edgecolor="red", facecolor='none', lw=6, linestyle='--')
    ax_left.add_patch(rect_highlight_window)
    window_data = input_matrix[i_start_calc:i_start_calc+kernel_size, j_start_calc:j_start_calc+kernel_size]
    max_val = np.max(window_data)    
    block_row_calc = window_row
    block_col_calc = window_col
    block_idx_right = block_row_calc * W_out + block_col_calc
    norm_right = block_norms[block_idx_right]
    cmap_right = block_cmaps[block_idx_right]    
    bg_luminance = norm_right(max_val)
    text_color_right = "white" if bg_luminance > 0.7 else "black"    
    right_texts[window_row][window_col].set_text(str(max_val))
    right_rects[window_row][window_col].set_facecolor(cmap_right(norm_right(max_val)))
    right_texts[window_row][window_col].set_color(text_color_right)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)    
    [p.remove() for p in ax_left.patches if p.get_linewidth() == 6 or p.get_facecolor() == (1.0, 0.0, 0.0, 1.0)]    
    return (*[t for row in left_texts for t in row], *[t for row in right_texts for t in row],
            *[r for row in left_rects for r in row], *[r for row in right_rects for r in row])


for frame in range(H_out * W_out):
    animate(frame)
iio.imwrite("maxpooling2d.gif", frames, duration=2000, loop=0)
plt.close(fig)