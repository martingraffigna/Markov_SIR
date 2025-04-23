import numpy as np
import pandas as pd
from sir_model import apply_sir
from sir_travel_prob import prob_builder
from mc_next_state import mc_next_state 
from builder import matrix_builder
'''
def init_state(read_file):
    """
    Initializes the state of the Markov chain from the input file.

    Parameters:
    - read_file (str): Path to the file to read.

    Returns:
    - ndarray: 3xN array representing the initial SIR population distribution.
    """
    data = pd.read_csv(read_file, header=None)#Assuming data.shape = Nx3 
    data = data.to_numpy().T
    return data

def matrix_builder(read_file):
    """
    Builds the transition matrix from the input file.

    Parameters:
    - read_file (str): Path to the file to read.

    Returns:
    - ndarray: 3xNxN array with transition probabilities to each city.
    """
    data = pd.read_csv(read_file, header=None)#Assuming data.shape = 3NxN 
    data = data.to_numpy()
    data = data.reshape(3, data.shape[1], data.shape[0]//3)
    return data

def sir_next_step(S, I, R, beta, gamma):
    N = S + I + R
    S_next = S - beta*S*I/N
    I_next = I + beta*S*I/N - gamma*I
    R_next = R + gamma*I
    return S_next, I_next, R_next

def mc_next_state(initial_state, transition_matrix):
    """
    Computes the next state in the Markov chain.

    Parameters:
    - initial_state (ndarray): 3XN array representing the initial SIR population distribution. (3,i)
    - transition_matrix (ndarray): 3xNxN array with transition probabilities to each city. (3,i,j)

    Returns:
    - ndarray: 3xN array representing the next state.
    """
    next_state = np.einsum('ci,cij->cj', initial_state, transition_matrix) # 
    return next_state

'''
beta = 0.5
gamma = 0.13
params = [beta, gamma]
days = 1
times = np.linspace(0, days, days+1)

S_prob = 0.6
I_prob = 0.8
R_prob = 0

TM = pd.read_csv("TransitionMatrixDBS.csv").to_numpy()[:,1:] #NxN, read the transition matrix
S_travelprob = prob_builder(TM,S_prob)  
I_travelprob = prob_builder(TM,I_prob)
R_travelprob = prob_builder(TM,R_prob)

S_tran = matrix_builder(TM, S_travelprob) 
I_tran = matrix_builder(TM, I_travelprob)
R_tran = matrix_builder(TM, R_travelprob)
SIR_tran = np.stack([S_tran,I_tran,R_tran],axis=0) #3xNxN


def main(days, filepath):
    state = pd.read_csv(filepath).to_numpy()

    for i in range(days):
        N = apply_sir(pd.DataFrame(state, columns=["S", "I", "R"]), params, times)
        state = mc_next_state(initial_state=N, transition_matrix=SIR_tran)
    return state