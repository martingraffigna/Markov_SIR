import numpy as np
import pandas as pd
import sir_travel_prob

def matrix_builder(transition_matrix, prop):
    """
    Create transition matrix for each region based on the probability of moving to another region for each SIR group.

    Parameters:
    - transition_matrix (csv file): NxN csv file with transition probabilities to each city.
    - prop (ndarray): NxN matrix with the probability of moving to another region for each SIR group.

    Returns:
    - ndarray: NxN array representing the transition matrix for each region for each SIR group.
    """
    return np.array(np.dot(transition_matrix,prop)) #NxN, multiply the transition matrix by the probability of moving to another region for each SIR group


'''
transition_matrix = "TransitionMatrixDBS.csv"
TM = pd.read_csv(transition_matrix).to_numpy()[:,1:] #NxN, read the transition matrix
S_travelprob = sir_travel_prob.S_travelprob
I_travelprob = sir_travel_prob.I_travelprob
R_travelprob = sir_travel_prob.R_travelprob

S_tran = matrix_builder(TM, S_travelprob) 
I_tran = matrix_builder(TM, I_travelprob)
R_tran = matrix_builder(TM, R_travelprob)
SIR_tran = np.stack([S_tran,I_tran,R_tran],axis=0) #3xNxN
'''