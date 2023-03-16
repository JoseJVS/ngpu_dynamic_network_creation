import sys
import ctypes
import numpy as np
import nestgpu as ngpu
from random import randrange
from time import perf_counter_ns
from argparse import ArgumentParser
from pathlib import Path
import os
from json import dump, dumps

# Get and check file path
parser = ArgumentParser()
parser.add_argument("file", type=str)
parser.add_argument("--path", type=str, default=None)
parser.add_argument("--seed", type=int, default=12345)
parser.add_argument("--algo", type=int, default=0)
parser.add_argument("--neurons", type=int, default=1000)
args = parser.parse_args()

if args.path is None:
    data_path = Path(os.getcwd())
else:
    data_path = Path(args.path)

file_name = args.file + ".json"
file_path = data_path / file_name

assert 0 <= args.algo and args.algo < 9 and data_path.is_dir() and not file_path.exists()

print(f"Arguments: {args}")

nl_dict = {
        0: "BlockStep",
        1: "CumulSum",
        2: "Simple",
        3: "ParallelInner",
        4: "ParallelOuter",
        5: "Frame1D",
        6: "Frame2D",
        7: "Smart1D",
        8: "Smart2D",
    }

# variable for spike recording
recording = False
# variable for plotting the raster plot
plotting = False
if plotting:
    recording = True

time_start = perf_counter_ns()

order = args.neurons//5
# set time resolution and NestedLoop algorithm
ngpu.SetTimeResolution(1.0)
if hasattr(ngpu, "SetNestedLoopAlgo"):
    ngpu.SetNestedLoopAlgo(args.algo)
else:
    print("Cannot set nested loop algorithm in NEST GPU version < 2.0")
# seed for GPU random numbers
ngpu.SetRandomSeed(args.seed)

# simulation time in seconds
sim_time = 10.0

n_receptors = 2

NE = 4 * order       # number of excitatory neurons
NI = 1 * order       # number of inhibitory neurons
n_neurons = NE + NI  # number of neurons in total
#print("Neurons: {}".format(n_neurons))

CE = 80     # number of excitatory synapses per neuron
CI = CE//4  # number of inhibitory synapses per neuron

fact=0.42
Wex = 0.5*fact
Win = -3.5*fact

poiss_rate = 1160.0
poiss_weight = 1.5

time_initialize = perf_counter_ns()

# create poisson generator
pg = ngpu.Create("poisson_generator")
ngpu.SetStatus(pg, "rate", poiss_rate)

# Create n_neurons neurons with n_receptor receptor ports
exc_neuron = ngpu.Create("izhikevich_psc_exp_2s", NE, n_receptors)
inh_neuron = ngpu.Create("izhikevich_psc_exp_2s", NI, n_receptors)

exc_params = {"a": 0.02, "b": 0.2, "c": -65.0, "d": 8.0}
inh_params = {"a": 0.1, "b": 0.2, "c": -65.0, "d": 2.0}
ngpu.SetStatus(exc_neuron, exc_params)
ngpu.SetStatus(inh_neuron, inh_params)

if recording:
    N_max_spike_times = 1000
    ngpu.ActivateRecSpikeTimes(exc_neuron, N_max_spike_times)
    ngpu.ActivateRecSpikeTimes(inh_neuron, N_max_spike_times)

time_create = perf_counter_ns()

# Excitatory connections
# connect excitatory neurons to port 0 of all neurons
# normally distributed delays, weight Wex and CE connections per neuron
exc_conn_dict={"rule": "fixed_indegree", "indegree": CE}
exc_syn_dict={"weight": Wex, "delay": {"distribution": "normal_clipped", "high": 20.0, "low": 1.0, "mu": 10.0, "sigma": 10.0}, "receptor":0}
ngpu.Connect(exc_neuron, exc_neuron, exc_conn_dict, exc_syn_dict)
ngpu.Connect(exc_neuron, inh_neuron, exc_conn_dict, exc_syn_dict)

# Inhibitory connections
# connect inhibitory neurons to port 1 of all neurons
# normally distributed delays, weight Win and CI connections per neuron
inh_conn_dict={"rule": "fixed_indegree", "indegree": CI}
inh_syn_dict={"weight": Win, "delay": {"distribution": "normal_clipped", "high": 20.0, "low": 1.0, "mu": 10.0, "sigma": 10.0}, "receptor":1}

ngpu.Connect(inh_neuron, exc_neuron, inh_conn_dict, inh_syn_dict)
ngpu.Connect(inh_neuron, inh_neuron, inh_conn_dict, inh_syn_dict)

#connect poisson generator to port 0 of all neurons
pg_conn_dict={"rule": "all_to_all"}
pg_syn_dict={"weight": poiss_weight, "delay": {"distribution": "normal_clipped", "high": 20.0, "low": 1.0, "mu": 10.0, "sigma": 10.0}, "receptor":0}

ngpu.Connect(pg, exc_neuron, pg_conn_dict, pg_syn_dict)
ngpu.Connect(pg, inh_neuron, pg_conn_dict, pg_syn_dict)

time_connect = perf_counter_ns()

ngpu.Calibrate()

time_calibrate = perf_counter_ns()

ngpu.Simulate(sim_time*1000.0)

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
    "nested_loop_algo": nl_dict[args.algo],
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
    exc_spike_times = ngpu.GetRecSpikeTimes(exc_neuron)
    inh_spike_times = ngpu.GetRecSpikeTimes(inh_neuron)
    # getting firing rate
    frE = np.zeros(NE)
    frI = np.zeros(NI)
    for i in range(len(exc_spike_times)):
        frE[i] = len(exc_spike_times[i])/(sim_time)
    for i in range(len(inh_spike_times)):
        frI[i] = len(inh_spike_times[i])/(sim_time)

    fr = np.concatenate((frE, frI))

    print("Mean firing rate [EXC]: {} +/- {} Hz".format(np.mean(frE), np.std(frE)))
    print("Mean firing rate [INH]: {} +/- {} Hz".format(np.mean(frI), np.std(frI)))
    print("Mean firing rate [TOT]: {} +/- {} Hz".format(np.mean(fr), np.std(fr)))

    if plotting:
        import matplotlib.pyplot as plt
        # raster plot of the spiking activity
        plt.figure()
        for i in range(len(exc_spike_times)):
            plt.plot(exc_spike_times[i], [i for j in range(len(exc_spike_times[i]))], ".", color="b")
        for i in range(len(inh_spike_times)):
            plt.plot(inh_spike_times[i], [i+NE for j in range(len(inh_spike_times[i]))], ".", color="r")
        plt.show()
