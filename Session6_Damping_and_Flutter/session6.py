import numpy as np
import scipy.linalg as linalg
from session3 import calc_eigenvalues_eigenvectors

def calc_non_conservative_eigenvalues_eigenvectors(M:np.array, C:np.array,K:np.array):
    """
    A function that computes the eigenvalues and eigenvectors
    based on the system parameter by reworking the equations of motion to a generalized eigenvalue problem

    Arguments:
    M, C, K -- system matrices of the MDOF system

    Returns:
    lamb -- The eigenvalues of the eigenvalue problem
    psi -- The eigenvectors of the eigenvalue problem
  
    
    """   
    
    if np.allclose(C, 0.0, atol=1e-14, rtol=0):
        # fall back to other  implementation (More stable)
        lamb_squared, psi = calc_eigenvalues_eigenvectors(K=K,M=M)
        
        return np.sqrt(-lamb_squared), psi
 
    # Rewriting the polynomial eigenvalue as a generalized eigenvalue problem
    
    ndof = np.shape(M)[0]
    A  = np.block([[K, np.zeros((ndof,ndof))],[np.zeros((ndof,ndof)), -M]])
    B  = np.block([[C, M],[M, np.zeros((ndof,ndof))]])
    lamb, psi = linalg.eig(A,-B)
    
    # Sorting the results from small to great (by default it is the opposite)
    
    lamb = lamb[::-1]
    psi = psi[:,::-1]

    return lamb[::2], psi[-ndof:,::2]