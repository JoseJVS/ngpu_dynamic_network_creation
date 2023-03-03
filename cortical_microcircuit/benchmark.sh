#!/bin/bash

#source $HOME/nestgpu/config.sh

# Best nested loop algorithm measured was BlockStep -> algo == 0
for algo in 0; do
	for seed in {0..9}; do
		sim_date=$(date +%F_%H-%M-%S)
		{ time python3  run_benchmark.py -o ../sim_output/results_$sim_date.json --algo=$algo --seed=$seed 2> ../sim_output/run_micro_eval_time_$sim_date.err; } &> ../sim_output/run_micro_eval_time_$sim_date.out
	done
done
