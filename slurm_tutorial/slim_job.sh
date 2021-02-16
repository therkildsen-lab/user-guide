#!/bin/bash -l
#SBATCH --ntasks=1
#SBATCH --mem=1000
#SBATCH --partition=regular
#SBATCH --job-name=slim_job
#SBATCH --output=slim_job.out
#SBATCH --array=1-7

# Run 7 different SLiM jobs in parallel.
# The parameters for each array job are set by the text file.

# Create and move to working directory for job:
WORKDIR=/SSD/$USER/$JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p $WORKDIR
cd $WORKDIR

# Copy files over to working directory:
BASE_DIR=/home/ikk23
cp $BASE_DIR/example/slim_files/merged_same_site_spatial.slim .
cp $BASE_DIR/example/slim_files/new_driver.py .
cp $BASE_DIR/example/slim_files/slimutil.py .
cp $BASE_DIR/example/slim_files/slim_job_params.txt .

# Include SLiM in the path
PATH=$PATH:/home/ikk23/SLiM/SLiM_build
export PATH

# Only the first .part file has the header
prog=`sed -n "${SLURM_ARRAY_TASK_ID}p" slim_job_params.txt`
$prog > slim_result_${SLURM_ARRAY_TASK_ID}.csv
cp slim_result_${SLURM_ARRAY_TASK_ID}.csv $BASE_DIR/example/results/

# Clean up working directory:
rm -r $WORKDIR
