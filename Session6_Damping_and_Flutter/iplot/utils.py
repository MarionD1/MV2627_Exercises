import numpy as np
import matplotlib.pyplot as plt 
import scipy.linalg as linalg



def build_3DOF_matrices(m:float,c:float,c1:float,k:float,k1:float):     
    M_mat=np.array([[m, 0, 0],
           [0, m, 0],
           [0, 0, m]])
    
    ###BEGIN SOLUTION
    
    K_mat=np.array([[k1+k, -k, 0],
           [-k, 2*k, -k],
           [0, -k, k]])
    C_mat=np.array([[c1+c, -c, 0],
            [-c, 2*c, -c],
            [0,-c,c]])
    ###END SOLUTION
    return M_mat, C_mat, K_mat
def calc_eigenvalues_eigenvectors(M:np.array, C:np.array,K:np.array):

    ndof = np.shape(M)[0]
    A  = np.block([[K, np.zeros((ndof,ndof))],[np.zeros((ndof,ndof)), -M]])
    B  = np.block([[C, M],[M, np.zeros((ndof,ndof))]])
    lamb, psi = linalg.eig(A,-B)
    
    # Sorting the results from small to great (by default it is the opposite)
    
    lamb = lamb[::-1]
    psi = psi[:,::-1]

    return lamb[::2], psi[-ndof:,::2]
def calc_xi(lamb):
    xi = -np.real(lamb)/np.abs(lamb)
    return xi

def get_frequnecy(lamb):
    return np.abs(lamb.imag)/(2*np.pi)


def damped_sdof_response(f, mu_j, omega_j, psi_j, xi_j=0, input_location=2, output_location=2):
    """
    A function that computes the frequency domain response of one mode j of an MDOF system

    Arguments:
    f -- the frequency vector
    mu_j -- modal mass of mode j
    omega_j -- natural frequency of mode j
    psi_j -- mode shape of mode j (n_dof x 1)
    xi_j -- modal damping of mode j

    Returns:
    x_0 - the frequency domain response fo the damped SDOF oscillator
    
    """   
    
    n_dof = len(psi_j)
    
    # Generate a force vector F and have a force F of amplitude 1 at the inputlocation
    F = np.zeros([n_dof, 1])
    F[input_location] = 1
    
    ###BEGIN SOLUTION
    
    omega = f*np.pi*2
    numerator = psi_j.T@F@psi_j[output_location]
    x_0 = numerator/(mu_j*(omega_j**2-np.power(omega,2)+2j*xi_j*omega*omega_j))
    
    ###END SOLUTION
    
    return x_0

def frequency_response_function(M:np.array, C:np.array, K:np.array, f= np.linspace(0,2,100), i=1,j=1):
    """
    A function that computes the Frequency Response Function from the system matrices

    Arguments:
    M,C,K -- system matrices of the MDOF system
    f -- the frequency for which the repsponse needs to be calculated
    i,j -- the specific element of the FRF matrix to be computed.

    Return: H_ij -- the i-th row and j-th column element of the FRF function at f
    """
    
    if not isinstance(f, np.ndarray):
        f = np.array([f])
    s = f*np.pi*2*1j
    
    M_s2 = np.outer(M,(s**2)).reshape(M.shape[0], -1, len(s))
    C_s = np.outer(C,(s**1)).reshape(M.shape[0], -1, len(s))
    K_s = np.outer(K,(s**0)).reshape(M.shape[0], -1, len(s))

    H_ij = []
    for s_i in range(len(s)):
        H_ij.append(np.linalg.inv((M_s2+C_s+K_s)[:,:,s_i])[i,j])
    
    return H_ij