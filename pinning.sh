# Fix numpy (numexpr) max number of supported threads
export NUMEXPR_MAX_THREADS=128

# Enable OpenMP pinning
export OMP_DISPLAY_ENV=VERBOSE
export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=TRUE
export OMP_NUM_THREADS=$1
