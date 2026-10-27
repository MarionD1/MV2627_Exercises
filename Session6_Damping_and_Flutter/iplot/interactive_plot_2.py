import numpy as np
from ipywidgets import interact, fixed

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from iplot.utils import build_3DOF_matrices, calc_eigenvalues_eigenvectors, calc_xi, get_frequnecy
M, C, K = build_3DOF_matrices(m=1, k=10, k1=10, c=0.1, c1=0.3)
lamb, psi = calc_eigenvalues_eigenvectors(M, C, K)  


# Define initial parameters
init_lossfactor = 0.01 * 2
f = np.arange(0.01, 1, 0.01)
omega = 2 * np.pi * f




# Create the figure and the line that we will manipulate
fig, axes = plt.subplots(1, 1)
axes.plot(get_frequnecy(lamb), calc_xi(lamb) * 100, marker='o', linestyle='', label='original')
line_t, = axes.plot([0, 1], init_lossfactor * np.array([100, 100]), color='gray', linestyle=':', label='Loss factor')

axes.set_ylabel('Damping ratio (%)')
axes.set_xlabel('Frequency (Hz)')
axes.grid(which='both', linestyle=':')
axes.set_ylim([0, 8])
plt.legend()

# Adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.4)

# Slider for the loss factor
ax_loss_factor = plt.axes([0.25, 0.15, 0.65, 0.03])
loss_factor_slider = Slider(
    ax=ax_loss_factor,
    label=r'loss factor ($\eta$)',
    valmin=0,
    valmax=0.1,
    valinit=init_lossfactor,
)

# The function to be called anytime a slider's value changes
def update(val):
    line_t.set_ydata(loss_factor_slider.val * np.array([100, 100]) / 2)
    fig.canvas.draw_idle()

# Register the update function with the slider
loss_factor_slider.on_changed(update)

# Reset Button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    loss_factor_slider.reset()

button.on_clicked(reset)

w = interact(update(fixed))