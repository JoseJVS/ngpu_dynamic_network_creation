# -*- coding: utf-8 -*-
#
# run_benchmark.py
# execute with:
#	python3 run_benchmark.py FILE [--path=PATH] [--seed=SEED] [--algo=ALGO]
#		with FILE the name of the file to output the JSON results
#		with PATH an optional argument to the path to the directory
#		    where data must be output. Defaults to "$PWD/data".
#		with SEED an optional integer argument for the simulation seed.
#			Defaults to 12345

""" pyCARL Two Population Benchmark
--------------------------------------------------



"""

###############################################################################
# Import the necessary modules and start the time measurements.

import carlsim as carl

from time import perf_counter_ns
from argparse import ArgumentParser
from pathlib import Path
from json import dump, dumps

# Get and check file path
parser = ArgumentParser()
#parser.add_argument("file", type=str)
#parser.add_argument("--path", type=str, default=None)
parser.add_argument("--conn_routine", type=str, default="full")
parser.add_argument("--pop_size", type=int, default=1000)
parser.add_argument("--seed", type=int, default=12345)
args = parser.parse_args()

#if args.path is None:
#    data_path = Path(sim_dict["data_path"])
#else:
#    data_path = Path(args.path)
#    sim_dict["data_path"] = str(data_path) + "/" # Path to str never ends with /

#file_name = args.file + ".json"
#file_path = data_path / file_name

assert (args.conn_routine == "full" or args.conn_routine == "one-to-one") and (args.pop_size > 0) #and data_path.is_dir() and not file_path.exists()

print(f"Arguments: {args}")

###############################################################################
# Construct network and do mock simulation

time_start = perf_counter_ns()

sim = carl.CARLsim("TwoPopulationBenchmark", carl.GPU_MODE, carl.USER, 0, args.seed)

g1 = sim.createGroup("pop1", args.pop_size, carl.EXCITATORY_NEURON, 0, carl.GPU_CORES)
sim.setNeuronParameters(grpId=g1, izh_a=0.02, izh_b=0.2, izh_c=-65.0, izh_d=8.0)

g2 = sim.createGroup("pop2", args.pop_size, carl.EXCITATORY_NEURON, 0, carl.GPU_CORES)
sim.setNeuronParameters(grpId=g2, izh_a=0.02, izh_b=0.2, izh_c=-65.0, izh_d=8.0)

sim.connect(g1, g2, args.conn_routine, carl.RangeWeight(1.0), 1.0, carl.RangeDelay(1), carl.RadiusRF(-1), carl.SYN_FIXED)
sim.connect(g2, g1, args.conn_routine, carl.RangeWeight(1.0), 1.0, carl.RangeDelay(1), carl.RadiusRF(-1), carl.SYN_FIXED)
sim.connect(g1, g1, args.conn_routine, carl.RangeWeight(1.0), 1.0, carl.RangeDelay(1), carl.RadiusRF(-1), carl.SYN_FIXED)
sim.connect(g2, g2, args.conn_routine, carl.RangeWeight(1.0), 1.0, carl.RangeDelay(1), carl.RadiusRF(-1), carl.SYN_FIXED)

sim.setConductances(False)

sim.setupNetwork()

time_construct = perf_counter_ns()

sim.runNetwork(nSec=0, nMsec=1)

time_simulate = perf_counter_ns()

###############################################################################
# Summarize time measurements.

time_dict = {
        "time_construct": time_construct - time_start,
        "time_simulate": time_simulate - time_construct,
        "time_total": time_simulate - time_start,
        }

conf_dict = {
    "conn_routine": args.conn_routine,
    "pop_size": args.pop_size,
    "seed": args.seed,
}

info_dict = {
        "conf": conf_dict,
        "timers": time_dict
    }

#with file_path.open("w") as f:
#    dump(info_dict, f, indent=4)

print(dumps(info_dict, indent=4))

