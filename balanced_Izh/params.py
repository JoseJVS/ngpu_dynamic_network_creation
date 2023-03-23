import os

"""
Network and Simulation parameters
"""

params = {
    "C_E" : 80,
    "C_I" : 20,
    "exc_params" : {'a': 0.02, 'b': 0.2, 'c': -65.0, 'd': 8.0},
    "inh_params" : {'a': 0.1, 'b': 0.2, 'c': -65.0, 'd': 2.0},
    "W_E": 6.0,#0.21,
    "W_I": -5.0,#-1.47,
    "W_P": 30.0,#1.5,
    "nu_P": 1.0,#1160.0,
    "delay_min": 1.0,
    "delay_max": 20.0,
    "delay_P": 1.0,
    "delay_mu": 10.0,
    "delay_sigma": 10.0,
    "sim_time": 10000.0
}


"""
Update default parameters with custom parameters
"""

def update_params(d, d2):
    for key in d2:
        if isinstance(d2[key], dict) and key in d:
            update_params(d[key], d2[key])
        else:
            d[key] = d2[key]


# check custom params correctness
def check_params(d, def_d):
    for key, val in d.items():
        if isinstance(val, dict):
            check_params(d[key], def_d[key])
        else:
            try:
                def_val = def_d[key]
            except KeyError:
                raise KeyError('Custom key {} not used.'.format(key))



