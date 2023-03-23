import sys
import ctypes
import numpy as np
import nest
from random import randrange
from time import perf_counter_ns
from argparse import ArgumentParser
from pathlib import Path
import os
from json import dump, dumps


# add network params using a dictionary for NEST and NEST GPU
sys.path.insert(1, '/home/gianmarco/new_ngpu_dyn/balanced_Izh')
from params import params


# Get and check file path
parser = ArgumentParser()
parser.add_argument("file", type=str)
parser.add_argument("--path", type=str, default=None)
parser.add_argument("--seed", type=int, default=12345)
parser.add_argument("--neurons", type=int, default=1000)
args = parser.parse_args()

if args.path is None:
    data_path = Path(os.getcwd())
else:
    data_path = Path(args.path)

file_name = args.file + ".json"
file_path = data_path / file_name

assert not file_path.exists()

print(f"Arguments: {args}")


# variable for spike recording
recording = True
# variable for plotting the raster plot
plotting = True
if plotting:
    recording = True

time_start = perf_counter_ns()

order = args.neurons//5
# set time resolution algorithm
nest.SetKernelStatus({"resolution": 1.0, "print_time": True})

# simulation time in seconds
sim_time = params["sim_time"]

NE = 4 * order       # number of excitatory neurons
NI = 1 * order       # number of inhibitory neurons
n_neurons = NE + NI  # number of neurons in total
#print("Neurons: {}".format(n_neurons))

CE = params["C_E"]     # number of excitatory synapses per neuron
CI = params["C_I"]     # number of inhibitory synapses per neuron

Wex = params["W_E"]
Win = params["W_I"]

poiss_rate = params["nu_P"]
poiss_weight = params["W_P"]

time_initialize = perf_counter_ns()

# create poisson generator
pg = nest.Create("poisson_generator")
nest.SetStatus(pg, "rate", poiss_rate)

# Create n_neurons neurons with n_receptor receptor ports
exc_neuron = nest.Create("izhikevich", NE)
inh_neuron = nest.Create("izhikevich", NI)

nest.SetStatus(exc_neuron, {"U_m": -13.0, "V_m": -70.0})
nest.SetStatus(inh_neuron, {"U_m": -13.0, "V_m": -70.0})

nest.SetStatus(exc_neuron, params["exc_params"])
nest.SetStatus(inh_neuron, params["inh_params"])

if recording:
    sr_E = nest.Create('spike_recorder')
    sr_I = nest.Create('spike_recorder')

time_create = perf_counter_ns()

# Excitatory connections
# connect excitatory neurons to port 0 of all neurons
# normally distributed delays, weight Wex and CE connections per neuron
exc_conn_dict={"rule": "fixed_indegree", "indegree": CE}
exc_syn_dict={"weight": Wex, "delay": nest.math.redraw(nest.random.normal(mean=params["delay_mu"], std=params["delay_sigma"]), min=params["delay_min"], max=params["delay_max"])}
nest.Connect(exc_neuron, exc_neuron, exc_conn_dict, exc_syn_dict)
nest.Connect(exc_neuron, inh_neuron, exc_conn_dict, exc_syn_dict)

# Inhibitory connections
# connect inhibitory neurons to port 1 of all neurons
# normally distributed delays, weight Win and CI connections per neuron
inh_conn_dict={"rule": "fixed_indegree", "indegree": int(CI*1.25)}
inh_syn_dict={"weight": Win, "delay": nest.math.redraw(nest.random.normal(mean=params["delay_mu"], std=params["delay_sigma"]), min=params["delay_min"], max=params["delay_max"])}

nest.Connect(inh_neuron, exc_neuron, inh_conn_dict, inh_syn_dict)
#nest.Connect(inh_neuron, inh_neuron, inh_conn_dict, inh_syn_dict)

#connect poisson generator to port 0 of all neurons
#pg_conn_dict={"rule": "all_to_all"}
pg_conn_dict={"rule": "fixed_indegree", "indegree": int(4.0*NE/5.0)}
pg_syn_dict={"weight": poiss_weight, "delay": params["delay_P"]}

nest.Connect(pg, exc_neuron, pg_conn_dict, pg_syn_dict)
#nest.Connect(pg, inh_neuron, pg_conn_dict, pg_syn_dict)

if recording:
    nest.Connect(exc_neuron, sr_E)
    nest.Connect(inh_neuron, sr_I)

time_connect = perf_counter_ns()

nest.Prepare()
nest.Cleanup()

time_calibrate = perf_counter_ns()

nest.Simulate(sim_time)

time_simulate = perf_counter_ns()

time_dict = {
        "time_initialize": time_initialize - time_start,
        "time_create": time_create - time_initialize,
        "time_connect": time_connect - time_create,
        "time_calibrate": time_calibrate - time_connect,
        "time_construct": time_calibrate - time_start,
        "time_simulate": time_simulate - time_calibrate,
        "time_total": time_simulate - time_start,
        }

conf_dict = {
    "num_neurons": args.neurons,
    "seed": args.seed,
}

info_dict = {
        "conf": conf_dict,
        "timers": time_dict
    }

with file_path.open("w") as f:
    dump(info_dict, f, indent=4)

print(dumps(info_dict, indent=4))

if recording:
    sr_E_data = sr_E.get("events")
    exc_spike = sr_E_data["senders"]
    ts_E = sr_E_data["times"]
    sr_I_data = sr_I.get("events")
    inh_spike = sr_I_data["senders"]
    ts_I = sr_I_data["times"]

    # getting firing rate
    frE = np.zeros(NE)
    frI = np.zeros(NI)
    for i in range(NE):
        frE[i] = list(exc_spike).count(i)/(sim_time/1000.0)
    for i in range(NI):
        frI[i] = list(inh_spike).count(i+NE)/(sim_time/1000.0)
    
    fr = np.concatenate((frE, frI))

    print("Mean firing rate [EXC]: {} +/- {} Hz".format(np.mean(frE), np.std(frE)))
    print("Mean firing rate [INH]: {} +/- {} Hz".format(np.mean(frI), np.std(frI)))
    print("Mean firing rate [TOT]: {} +/- {} Hz".format(np.mean(fr), np.std(fr)))

    if plotting:
        import matplotlib.pyplot as plt
        # raster plot of the spiking activity
        plt.figure()
        plt.plot(ts_E, exc_spike,  ".", color="b")
        plt.plot(ts_I, inh_spike, ".", color="r")
        plt.show()
