#!/bin/bash
# Benchmarking script for executing 10 simulations
# with different random generation seeds with GeNN
# execute with:
#	bash benchmark.sh

# Number of CPU cores in system
cores=128

# Number of MPI processes ONLY USED BY SLURM
procs=1

# Number of threads per process
# Fill the whole system by assigning as many possible threads equally to all MPI processes
threads=$( expr $cores / $procs )

# Top of output files hierarchy
data_path=data

# Experiment identifier
sim_id=$(date +%F_%H-%M-%S)

# For seeds 123450 123451 123452 123453...123459
for seed in {0..9}; do
	seed=12345$seed

	# Simulation identifier
	run_id=$seed\_$sim_id
	echo "Benchmark: seed $seed, id $sim_id"

	# For each seed a new directory is created
	run_path=$data_path/seed_$seed\_id_$sim_id
	if [ -z $( readlink -e $run_path ) ]; then
		mkdir -p $run_path
	elif [ ! -d $run_path ]; then
		echo "ERROR: Could not create run directory"
		exit 1
	fi

	# Run locally
	python3 run_benchmark.py benchmark_times_$run_id --path=$run_path --seed=$seed 2> $data_path/run_benchmark_$run_id.err 1> $data_path/run_benchmark_$run_id.out

	# Run with slurm
	# srun --ntasks-per-node=$procs --cpus-per-task=$threads --threads-per-core=1 --cpu-bind=verbose,rank --error=$data_path/run_benchmark_$run_id.err --output=$data_path/run_benchmark_$run_id.out python3 run_benchmark.py benchmark_times_$run_id --path=$run_path --seed=$seed

	# Delete build directory
	rm -rf potjans_microcircuit_CODE
done

python3 gather_data.py $data_path --out=$data_path/benchmark_data_$sim_id.json
