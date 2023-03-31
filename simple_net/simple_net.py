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
parser.add_argument("--connectivity", type=str, default="all_to_all")
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

time_start = perf_counter_ns()

# set time resolution and NestedLoop algorithm
ngpu.SetTimeResolution(1.0)
if hasattr(ngpu, "SetNestedLoopAlgo"):
    ngpu.SetNestedLoopAlgo(args.algo)
else:
    print("Cannot set nested loop algorithm in NEST GPU version < 2.0")
# seed for GPU random numbers
ngpu.SetRandomSeed(args.seed)

N1 = args.neurons       # number of excitatory neurons
N2 = args.neurons       # number of inhibitory neurons

# synaptic weight
w = 1.0
# synaptic delay
d = 1.0
# neuron parameters
neur_params = {'a': 0.02, 'b': 0.2, 'c': -65.0, 'd': 8.0}

time_initialize = perf_counter_ns()

# Create N1+N2 neurons
neuron_pop1 = ngpu.Create("izhikevich", N1)
neuron_pop2 = ngpu.Create("izhikevich", N2)

# set the neuron parameters
ngpu.SetStatus(neuron_pop1, neur_params)
ngpu.SetStatus(neuron_pop2, neur_params)

time_create = perf_counter_ns()

# connect population 1 to 2 and vice versa
# can be all_to_all or one_to_one
conn_dict={"rule": args.connectivity}
syn_dict={"weight": w, "delay": d}
ngpu.Connect(neuron_pop1, neuron_pop2, conn_dict, syn_dict)
ngpu.Connect(neuron_pop2, neuron_pop1, conn_dict, syn_dict)
# recurrent connections
ngpu.Connect(neuron_pop1, neuron_pop1, conn_dict, syn_dict)
ngpu.Connect(neuron_pop2, neuron_pop2, conn_dict, syn_dict)

time_connect = perf_counter_ns()

ngpu.Calibrate()

time_calibrate = perf_counter_ns()

ngpu.Simulate(1.0)

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
    "connectivity": args.connectivity,
    "seed": args.seed,
}

info_dict = {
        "conf": conf_dict,
        "timers": time_dict
    }

with file_path.open("w") as f:
    dump(info_dict, f, indent=4)

print(dumps(info_dict, indent=4))
