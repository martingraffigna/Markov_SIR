import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp, ode

# SIR ODE model
# parameters: beta, gamma
# init: S, I, R
# times: array of time points
# returns: DataFrame with columns t, S, I, R
def sir_ode(times, init, params):
    beta, gamma = params
    S, I, R = init
    N = S + I + R
    # odes
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# run SIR model for a single region
# init: S, I, R
# params: beta, gamma
# times: array of time points
# returns: final values S, I, R at the last time point
def run_sir(init, params, times):
    sir_sol = solve_ivp(fun=lambda t, y: sir_ode(t, y, params), t_span=[times[0], times[-1]], y0=init, t_eval=times)
    sir_df = pd.DataFrame({"S": sir_sol["y"][0], "I": sir_sol["y"][1], "R": sir_sol["y"][2]})
    final_ratio = sir_df.iloc[-1].values
    # can add rounding if needed
    return final_ratio

# run SIR model for multiple regions
# regions_sir: DataFrame with columns region, S, I, R
# params: beta, gamma
# times: array of time points
# returns: DataFrame with columns region, S, I, R after runing SIR ODE for each region
def apply_sir(regions_sir, params, times):
    sir_df = []
    regions_sir = regions_sir.copy()
    #regions_sir = regions_sir.drop(columns=["region"])
    sir_df = regions_sir.apply(run_sir, axis=1, args=(params, times))
    sir_df = pd.DataFrame(sir_df.tolist(), columns=["S", "I", "R"])
    return sir_df


# example usage:
'''
params = [0.1, 0.05]
init = [0.99, 0.01, 0]
times = np.linspace(0, 100, 1000)
sir_sol = solve_ivp(fun=lambda t, y: sir_ode(t, y, params), t_span=[times[0], times[-1]], y0=init, t_eval=times)
sir_df = pd.DataFrame({"S": sir_sol["y"][0], "I": sir_sol["y"][1], "R": sir_sol["y"][2]})
print(sir_df.iloc[-1].values)

params = [0.1, 0.05]
times = np.linspace(0, 100, 1000)
dummy_matrix = [[1, 0.99, 0.1, 0], [2, 0.98, 0.02, 0], [3, 0.97, 0.03, 0]]
N = apply_sir(pd.DataFrame(dummy_matrix, columns=["region", "S", "I", "R"]), params, times)
print(N)

'''
init_state = pd.read_csv('init_state.csv').to_numpy()
params = [0.1, 0.05]
times = np.linspace(0, 1, 2)
N = apply_sir(pd.DataFrame(init_state, columns=["S", "I", "R"]), params, times)
