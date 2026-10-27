from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
from iplot.utils import build_3DOF_matrices, calc_eigenvalues_eigenvectors, calc_xi

M, C, K = build_3DOF_matrices(m=1, k=10, k1=10, c=0.1, c1=0.3)

# Define initial parameters
init_alpha = 0.01
init_beta = 0.01

f = np.arange(0.01,1,0.01)
omega = 2*np.pi*f

def get_frequency(lamb):
    return np.abs(lamb)/2/np.pi

C_r =init_alpha*K + init_beta*M
lamb, psi = calc_eigenvalues_eigenvectors(M,C,K)

# Create the figure and the line that we will manipulate

fig, axes = plt.subplots(1,1)
plt.plot(get_frequency(lamb), calc_xi(lamb)*100, marker='o', linestyle='', label='original')
line_t, = plt.plot(f,1/2*(init_alpha*omega+init_beta/omega)*100, color='gray', linestyle=':', label='Rayleigh')

axes.set_ylabel('Damping ratio (%)')
axes.set_xlabel('Frequency (Hz)')
axes.grid(which='both', linestyle=':')

plt.legend()


# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.4)


axmass = plt.axes([0.25, 0.15, 0.65, 0.03])
alpha_slider = Slider(
    ax=axmass,
    label='alpha',
    valmin=0,
    valmax=0.1,
    valinit=init_alpha,
)
axstifness=plt.axes([0.25, 0.1, 0.65, 0.03])
beta_slider = Slider(
    ax=axstifness,
    label="beta",
    valmin=0,
    valmax=.1,
    valinit=init_beta,
)

# The function to be called anytime a slider's value changes
def update(fixed):
    C_r =alpha_slider.val*K + beta_slider.val*M
    
    rayleigh = 1/2*(alpha_slider.val*omega+beta_slider.val/omega)*100
    line_t.set_ydata(rayleigh)
   
    fig.canvas.draw_idle()

# register the update function with each slider
alpha_slider.on_changed(update)
_= beta_slider.on_changed(update)

# Reset Button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    alpha_slider.reset()
    beta_slider.reset()
button.on_clicked(reset)

w = interact(update(fixed))