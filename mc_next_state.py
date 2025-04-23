import numpy as np
import pandas as pd
import builder

def mc_next_state(initial_state, transition_matrix):
    """
    Computes the next state in the Markov chain.

    Parameters:
    - initial_state (ndarray): 3XN array representing the initial SIR population distribution. (3,i)
    - transition_matrix (ndarray): 3xNxN array with transition probabilities to each city. (3,i,j)

    Returns:
    - ndarray: 3xN array representing the next state.
    """

    next_state = np.einsum('ic,cij->jc', initial_state, transition_matrix) # 
    return next_state

'''
SIR_tran = builder.SIR_tran
N = pd.read_csv('init_state.csv').to_numpy() # 3xN
print(np.sum(N, axis=0)) # sum of each row (S,I,R) in the initial state
state = mc_next_state(initial_state=N,transition_matrix=SIR_tran) # 3xN
print(np.sum(state, axis=0)) # sum of each row (S,I,R) in the next state
'''