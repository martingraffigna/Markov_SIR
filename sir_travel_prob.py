# make travel probability matrix for each type of SIR group
# example matrix:
# S_travelprob = 0.4, S_stayathome = 0.6
# for susceptible patients, they are not infectious and they can travel but are suscueptible
#                           so they are cautious about traveling => travel probability = 0.4
# for infected patients, they are infectious and possibly symptomatic, so they should stay at home
#                        but we must also account for those who are asymptomatic and can travel => travel probability = 0.2
# for recovered patients, they are not infectious and they have antibodies so they are not susceptible
#                         to the disease and therefore can travel freely => travel probability = 1 (identity matrix, same as transition matrix)
import numpy as np
import pandas as pd
def prob_builder(TM,prob):
  n = TM.shape[1]
  mask = TM>0
  eye = np.eye(n)
  rest = np.ones((n,n)) - eye
  normalizer = (1-prob)/(mask.sum(axis=1)-1)  
  rest = rest*normalizer[:,np.newaxis]
  fill = np.zeros((n,n))
  fill[mask]= rest[mask]
  return eye*prob + fill


S_prob = 0.6
I_prob = 0.8
R_prob = 0
n = 159
TM = pd.read_csv("TransitionMatrixDBS.csv").to_numpy()[:,1:] #NxN, read the transition matrix
S_travelprob = prob_builder(TM,S_prob)
I_travelprob = prob_builder(TM,I_prob)
R_travelprob = prob_builder(TM,R_prob)
#SIR_travelprob = np.stack([S_travelprob,I_travelprob,R_travelprob],axis=0) #3xNxN