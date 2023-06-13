# -*- coding: utf-8 -*-
#
# run_benchmark.py
# execute with:
#	python3 run_benchmark.py FILE [--path=PATH] [--seed=SEED] [--algo=ALGO]
#		with FILE the name of the file to output the JSON results.
#		with PATH an optional argument to the path to the directory
#		    where data must be output. Defaults to "$PWD/data".
#		with SEED an optional integer argument for the simulation seed.
#			Defaults to 12345
#		with ALGO an optional integer argument for the number nested loop algorithm to be used.
#			Defaults to 0.
#           Avaiable nested loop algorithms:
#           0: BlockStep
#           1: CumulSum
#           2: Simple
#           3: ParallelInner
#           4: ParallelOuter
#           5: Frame1D
#           6: Frame2D
#           7: Smart1D
#           8: Smart2D

"""
--------------------------------------------------

This is an example script for running the microcircuit model.
This version is adjusted for benchmark simulations. Since spikes are
usually not recorded in this scenario, the evaluation part with plotting of
'run_microcircuit.py' is not performed here.

"""

###############################################################################
# Import the necessary modules and start the time measurements.

from stimulus_params import stim_dict
from network_params import net_dict
from sim_params import sim_dict
import network
import nestgpu as ngpu

from time import perf_counter_ns
from argparse import ArgumentParser
from pathlib import Path
from json import dump, dumps

# Get and check file path
parser = ArgumentParser()
parser.add_argument("file", type=str)
parser.add_argument("--path", type=str, default=None)
parser.add_argument("--seed", type=int, default=12345)
parser.add_argument("--algo", type=int, default=0)
args = parser.parse_args()

if args.path is None:
    data_path = Path(sim_dict["data_path"])
else:
    data_path = Path(args.path)
    sim_dict["data_path"] = str(data_path) + "/" # Path to str never ends with /

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

###############################################################################
# Initialize the network with simulation, network and stimulation parameters,
# then create and connect all nodes, and finally simulate.
# The times for a presimulation and the main simulation are taken
# independently. A presimulation is useful because the spike activity typically
# exhibits a startup transient. In benchmark simulations, this transient should
# be excluded from a time measurement of the state propagation phase. Besides,
# statistical measures of the spike activity should only be computed after the
# transient has passed.

sim_dict.update({
    't_presim': 0.1,
    't_sim': 10000.,
    'rec_dev': [],
    'master_seed': args.seed})

net_dict.update({
    'N_scaling': 1.,
    'K_scaling': 1.,
    'poisson_input': True,
    'V0_type': 'optimized'})

time_start = perf_counter_ns()

net = network.Network(sim_dict, net_dict, stim_dict)

if hasattr(ngpu, "SetNestedLoopAlgo"):
    ngpu.SetNestedLoopAlgo(args.algo)
else:
    print("Cannot set nested loop algorithm in NEST GPU version < 2.0")

time_initialize = perf_counter_ns()

net.create()
time_create = perf_counter_ns()

net.connect()
time_connect = perf_counter_ns()

net.simulate(sim_dict['t_presim'])
time_calibrate = perf_counter_ns()

net.simulate(sim_dict['t_sim'])
time_simulate = perf_counter_ns()

###############################################################################
# Summarize time measurements. Rank 0 usually takes longest because of print
# calls.

time_dict = {
        "time_initialize": time_initialize - time_start,
        "time_create": time_create - time_initialize,
        "time_connect": time_connect - time_create,
        "time_calibrate": time_calibrate - time_connect,
        "time_construct": time_calibrate - time_start,
        "time_simulate": time_simulate - time_calibrate,
        "time_total": time_simulate - time_start,
        }

num_neurons = net.get_network_size()
conf_dict = {
    "nested_loop_algo": nl_dict[args.algo],
    "num_neurons": num_neurons,
    "seed": args.seed,
}

info_dict = {
        "conf": conf_dict,
        "timers": time_dict
    }

with file_path.open("w") as f:
    dump(info_dict, f, indent=4)

print(dumps(info_dict, indent=4))

