#!/bin/bash -x
#SBATCH --account=jinb33
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00
#SBATCH --partition=dc-gpu
#SBATCH --gres=gpu:1
#SBATCH --output=/p/project/cjinb33/villamar1/nestgpu/runners/dnc_paper/sim_output/run_benchmark_%j.out
#SBATCH --error=/p/project/cjinb33/villamar1/nestgpu/runners/dnc_paper/sim_output/run_benchmark_%j.err
# *** start of job script ***
# Note: The current working directory at this point is
# the directory where sbatch was executed.

source /p/project/cjinb33/villamar1/nestgpu/config.sh

data_path=$1
if [ -z $data_path ]; then
	data_path=../sim_output
fi

seed=$2
if [ -z $seed ]; then
	seed=12345
fi

algo=$3
if [ -z $algo ]; then
	algo=0
fi

srun time python3 run_benchmark.py benchmark_times_${SLURM_JOBID}.json --path=$data_path --seed=$seed --algo=$algo
