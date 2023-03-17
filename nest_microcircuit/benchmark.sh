#!/bin/bash
# Benchmarking script for executing 10 simulations
# with different random generation seeds with NEST
# NEST requires OpenMP pinning and MPI binding for good performance.
# execute with:
#	bash benchmark.sh [procs]
#		with procs an optional integer argument representing number of MPI processes
#			defaults to 8

# Number of CPU cores in system
cores=128

# Number of MPI processes
procs=$1
if [ -z $procs ]; then
	procs=8
fi

# Number of threads per process
# Fill the whole system by assigning as many possible threads equally to all MPI processes
threads=$( expr $cores / $procs )

# Top of output files hierarchy
data_path=data

# Experiment identifier
sim_id=$(date +%F_%H-%M-%S)

# jemalloc library path to be exported with system specific path
# export LD_PRELOAD=...

# Fix numpy (numexpr) max number of supported threads
export NUMEXPR_MAX_THREADS=$cores

# Enable OpenMP pinning
export OMP_DISPLAY_ENV=VERBOSE
export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=TRUE
export OMP_NUM_THREADS=$threads

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

	# Run locally, using MPI process pinning to each L3cache partition, placed as distant as possible NEEDS TESTING
	# mpirun -n $procs --bind-to L3cache --map-by distance --report-bindings python3 run_benchmark.py benchmark_times_$run_id --path=$run_path --seed=$seed --procs=$procs --threads=$threads 2> $data_path/run_benchmark_$run_id.err 1> $data_path/run_benchmark_$run_id.out

	# Run with slurm, and let it handle the pinning
	srun --ntasks-per-node=$procs --cpus-per-task=$threads --threads-per-core=1 --cpu-bind=verbose,rank --error=$data_path/run_benchmark_$run_id.err --output=$data_path/run_benchmark_$run_id.out python3 run_benchmark.py benchmark_times_$run_id --path=$run_path --seed=$seed --threads=$threads

	# Merge json output of each MPI process into one json file and delete per rank files
	python3 merge_data.py $run_path --out=$run_path/benchmark_times_$run_id.json --cleanup
done

python3 gather_data.py $data_path --out=$data_path/benchmark_data_$sim_id.json
