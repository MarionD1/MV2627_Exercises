from matplotlib.widgets import Slider, Button
import numpy as np
from ipywidgets import interact, fixed

from iplot.utils import build_3DOF_matrices, calc_eigenvalues_eigenvectors, calc_xi , damped_sdof_response, frequency_response_function
import matplotlib.pyplot as plt

from ipywidgets import interact
from matplotlib.widgets import Slider, Button
# Define initial parameters
init_c = 1
M, C, K = build_3DOF_matrices(m=1, k=10, k1=10, c=0.1, c1=0.3)
lamb_c, psi_c = calc_eigenvalues_eigenvectors(M,C*0,K) # To calculate the conservative system very simply make C=0
f= np.arange(0,1,0.01)
omega = 2*np.pi*f
lamb_c, psi_c = calc_eigenvalues_eigenvectors(M,C*0,K) # To calculate the conservative system very simply make C=0

M_prj = psi_c.T@M@psi_c

def get_modal_damping_H33(c_multi):
    lamb_d, _ = calc_eigenvalues_eigenvectors(M,C*c_multi,K) # To calculate the conservative system very simply make C=0
    
    all_sdofs=[]
    for j in [0,1,2]:
        # Tip You can just copy the reponse for assignment 3.3 and change the loss_factor into the actual xi_j
        psi_j = psi_c[:,j].reshape(-1, 1)

        mu_j = M_prj[j,j]
        omega_j = abs(lamb_d[j])
        input_location = 2
        all_sdofs.append(damped_sdof_response(f, mu_j, omega_j, psi_j, xi_j=calc_xi(lamb_d[j]))) # This is the only line that differs from assignment 3.3 (calc_xi)
    return np.sum(all_sdofs, axis=0)
    
    

# Create the figure and the line that we will manipulate
H_33 = frequency_response_function(M,C,K,i=2,j=2, f=f)
H_33_d = frequency_response_function(M,C*init_c,K,i=2,j=2, f=f)

x_all_modal_damping = get_modal_damping_H33(init_c)




fig, axes = plt.subplots(1,1)
plt.semilogy(f, np.abs(H_33), color='gray', linestyle='-', label='original')

line_d, = plt.semilogy(f, np.abs(H_33_d), color='black', linestyle='-', label='Damped', linewidth=3)
line_md, = plt.semilogy(f, np.abs(x_all_modal_damping), color='tab:orange', linestyle='-', label='Modal damping')

# line_t, = plt.plot(f,1/2*(init_alpha*omega+init_beta/omega)*100, color='gray', linestyle=':', label='Rayleigh')

axes.set_ylabel('$|X_3(f)|$')
axes.set_xlabel('Frequency (Hz)')
axes.grid(which='both', linestyle=':')

plt.legend()


# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.4)


axmass = plt.axes([0.25, 0.15, 0.65, 0.03])
c_slider = Slider(
    ax=axmass,
    label='damping multiplier',
    valmin=0.1,
    valmax=5,
    valinit=init_c,
)


# The function to be called anytime a slider's value changes
def update(fixed):
    print('y')
    H_33_d = frequency_response_function(M,C*c_slider.val,K,i=2,j=2, f=f)
    x_all_modal_damping = get_modal_damping_H33(c_slider.val)

    
    line_d.set_ydata(np.abs(H_33_d))
    line_md.set_ydata(np.abs(x_all_modal_damping))

   
    fig.canvas.draw_idle()

# register the update function with each slider
_= c_slider.on_changed(update)

# Reset Button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    c_slider.reset()
button.on_clicked(reset)

w = interact(update(fixed))