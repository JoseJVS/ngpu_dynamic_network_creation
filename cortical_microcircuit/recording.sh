#!/bin/bash

for seed in {0..9}; do
	# Best nested loop algorithm measured was BlockStep -> algo == 0
	for algo in 0; do
		echo "Recording: seed $seed, algo $algo"
		data_path=../sim_output/recording-seed-$seed-algo-$algo
		mkdir $data_path
		sim_date=$(date +%F_%H-%M-%S)
		{ time python3 run_recording.py recording_times_$sim_date.json --path=$data_path --seed=$seed --algo=$algo 2> ../sim_output/run_recording_$sim_date.err; } &> ../sim_output/run_recording_$sim_date.out
		# For slurm change above command to this:
		# sbatch sbatch_benchmark.sh $data_path $seed $algo
	done
done
