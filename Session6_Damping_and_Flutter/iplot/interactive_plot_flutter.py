
import numpy as np
from iplot.utils import *
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button
from session2 import impulse_response
def white_noise_force(no_samples):
    """
    A function that serves to generate a zero-mean white noise signal of a length 'no_samples'.
    """
    
    ###BEGIN SOLUTION
    f = np.random.normal(0,1, size=no_samples)
    ###END SOLUTION
    
    return f
def sdof_force_response(m:float,c:float,k:float,t:np.ndarray, f:np.ndarray):
    """
    Implement the reponse of an SDOF system to 
    
    Arguments:
    m, c and k -- Parameter of the system 
                -- m is in kg
                -- c is in N.s.m^-1
                -- k is in N.m^-1
    t          -- Time vector, containing the timesteps 
    f          -- Force vector, i.e. white noise
    
    Returns:
    x -- the response of the SDOF system for the timesteps in the Time vector t
    """
    ###BEGIN SOLUTION
    h = impulse_response(m=m, c=c, k=k, t=t)
    x = np.convolve(h, f, mode='full')[:len(f)] 
    ###END SOLUTION

    return x
    

def calc_roots(m,c,k):
    return  np.roots([m, c, k])
init_k = 16
init_m = 1
init_c = 0.1

# Create the figure and the line that we will manipulate
no_samples = 1000
f_white = white_noise_force(no_samples)

fig, ax = plt.subplots(1,2)
t = np.arange(start=0,stop=100,step=0.02)
###BEGIN SOLUTION

f_white_noise = white_noise_force(len(t))

response = sdof_force_response(m=init_m, c=init_c, k=init_k, f=f_white_noise, t=t)
sdof_lambda = calc_roots(m=init_m,k=init_k,c=init_c)

line, = ax[0].plot(t,response, lw=2)
line_pole, =  ax[1].plot(np.array([0,np.real(sdof_lambda[0])]),np.array([0,np.imag(sdof_lambda[0])]), color='blue', marker='.', linestyle=':')

ax[0].set_ylabel('x(t)')
ax[0].grid(which='both', linestyle=':')
ax[0].set_xlabel('Time (s)')

ax[1].set_xlabel('real($\lambda$)')
ax[1].set_ylabel('imag($\lambda$)')
ax[1].set_xlim([-0.2,0.1])
ax[1].set_ylim([0,5])


ax[1].grid(which='both', linestyle=':')
plt.axvline(0, color='r')
plt.axhline(0, color='k')

ax[0]
# adjust the main plot to make room for the sliders
plt.subplots_adjust(bottom=0.3)

    
axc = plt.axes([0.25, 0.1, 0.65, 0.03])
k_slider = Slider(
    ax=axc,
    label="Stifness (N/m)",
    valmin=0.005,
    valmax=20,
    valinit=init_k,
)
    
    

axc = plt.axes([0.25, 0.15, 0.65, 0.03])
c_slider = Slider(
    ax=axc,
    label="Damping (N/(m*s))",
    valmin=-0.2,
    valmax=0.2,
    valinit=init_c,
)


eigenvalue_history = []
# The function to be called anytime a slider's value changes
def update(fixed):
    response = sdof_force_response(m=init_m, c=c_slider.val, k=k_slider.val, f=f_white_noise, t=t)
    
    sdof_lambda = calc_roots(m=init_m, c=c_slider.val, k=k_slider.val)
    
    line_pole.set_ydata([0,np.imag(sdof_lambda[0])])
    line_pole.set_xdata([0,np.real(sdof_lambda[0])])

    ax[0].relim()
    ax[0].autoscale_view()

    line.set_ydata(response)

    fig.canvas.draw_idle()

# register the update function with each slider
c_slider.on_changed(update)
k_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])

button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    k_slider.reset()
    c_slider.reset()

button.on_clicked(reset)


w = interact(update(fixed))