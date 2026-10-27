import numpy as np

# cell metadata=autograded-answer

def convert_pulsation(w:float):
    """
    Implement a function that the frequency from a pulsation omega 
    
    Arguments:
    w -- the pulsation 

    Returns:
    f -- the frequency in Hz
    """   
    
    ### BEGIN SOLUTION
    f = w/2/np.pi
    ### END SOLUTION

    return f

def calcXi(m:float, c:float, k:float):
    """
    Implement the expression of Xi
    
    Arguments:
    m,c,k -- parameter of the SDOF system
    
    Returns:
    xi -- the value of Xi, computed using the formula seen in the course
    """   

    ### BEGIN SOLUTION
    xi= c/(2*np.sqrt(m*k))
    ### END SOLUTION
    
    return xi
def calcW_d(w_n:float,xi:float):
    """
    Implement the expression of W_n
    
    Arguments:
    wn,xi -- properties of the SDOF system
    
    Returns:
    w_n -- the value of w_n, computed using the formula seen in the course
    """   

    ### BEGIN SOLUTION
    w_d = w_n*np.sqrt(1-xi**2)
    ### END SOLUTION
    return w_d
def calcW_n(k:float,m:float):
    """
    Implement the expression of W_n

    Arguments:
    k, m -- parameters of the SDOF system

    Returns:
    w_n -- the value of w_n, computed using the formula seen in the course
    """   

    ### BEGIN SOLUTION
    w_n = np.sqrt(k/m)
    ### END SOLUTION

    return w_n
    
def impulse_response(m:float,c:float,k:float,t:np.ndarray):
    """
    Implement the SDOF impulse response 
    
    Arguments:
    m, c and k -- Parameter of the system 
                -- m is in kg
                -- c is in N.s.m^-1
                -- k is in N.m^-1
    t          -- Time vector, containing the timesteps 
    
    Returns:
    h -- the value of function h for the timesteps in the Time vector t, computed using 
        expression of the impulse response
    -----------------------------
    tips :  1.call the function defined above to compute Xi and Wn and 
              save them in a local variable
            2.define a variable wd first
            3.use np.exp and np.sin
    -----------------------------
    """

    xi=calcXi(m=m, c=c, k=k)
    
    w_n=calcW_n(m=m, k=k)
    
    w_d= calcW_d(w_n, xi)
    
    ### BEGIN SOLUTION
    h=1/(m*w_d)*np.exp(-xi*w_n*t)*np.sin(w_d*t)
    ### END SOLUTION
    return h