#!/bin/bash

# Number of MPI processes ONLY USED BY SLURM
procs=1

# Number of threads per process
threads=$( expr 128 / $procs )

# Nested loop algorithm
# 0: BlockStep
# 1: CumulSum
# 2: Simple
# 3: ParallelInner
# 4: ParallelOuter
# 5: Frame1D
# 6: Frame2D
# 7: Smart1D
# 8: Smart2D
nl_algo=0

# Top of output files hierarchy
data_path=data

# Experiment identifier
sim_id=$(date +%F_%H-%M-%S)

# Fix numpy (numexpr) max number of supported threads
export NUMEXPR_MAX_THREADS=128

# Enable OpenMP pinning ONLY USED BY NEST GPU KERNEL FOR NETWORK CREATION
export OMP_DISPLAY_ENV=VERBOSE
export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=TRUE
export OMP_NUM_THREADS=$threads

# For seeds 123450 123451 123452 123453...123459
for neur in 1000 10000 100000 1000000; do
    for seed in {0..9}; do
        seed=12345$seed

        # Simulation identifier
        run_id=$neur\_$seed\_$sim_id
        echo "Benchmark: neurons $neur seed $seed, id $sim_id"

        # For each seed a new directory is created
        run_path=$data_path/$neur\_neurons/seed_$seed\_id_$sim_id
        if [ -z $( readlink -e $run_path ) ]; then
            mkdir -p $run_path
        elif [ ! -d $run_path ]; then
            echo "ERROR: Could not create run directory"
            exit 1
        fi

        # Run locally
        python3 balanced_Izh.py benchmark_times_$run_id --neurons=$neur --path=$run_path --seed=$seed --algo=$nl_algo 2> $data_path/run_benchmark_$run_id.err 1> $data_path/run_benchmark_$run_id.out

        # Run with slurm
        # srun --ntasks-per-node=$procs --cpus-per-task=$threads --threads-per-core=1 --cpu-bind=verbose,rank --error=$data_path/run_benchmark_$run_id.err --output=$data_path/run_benchmark_$run_id.out python3 run_benchmark.py benchmark_times_$run_id --path=$run_path --seed=$seed --algo=$nl_algo

    done

    python3 gather_data.py $data_path/$neur\_neurons --out=$data_path/benchmark_data_$neur\_$sim_id.json

done

