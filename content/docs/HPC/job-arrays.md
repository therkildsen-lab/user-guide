---
title: Job Arrays
type: docs
sidebar:
  open: true
---

## Job arrays

- If you want to run an identical program 10 times, instead of using afor-loop, you can submit the script as a job array of length 10.This is controlled by the header: `#SBATCH --array=1-10`
- Each array job will get its own unique ID, `SLURM_ARRAY_TASK_ID`,that you can make use of in your script.
- If you want each job in a 1-10 array to run something different, youcan create a text file with 10 lines and have each line specify thecommand you want to run.- Make sure to copy this text file over to the temporary working   directory!- In the shell script, write:

```bash
# go to the <SLURM_ARRAY_TASK_ID> line of the job_parameters.txt file
# and run this command
# for example, this line could read `python my_script.py 4`
prog=`sed -n "${SLURM_ARRAY_TASK_ID}p" job_parameters.txt`
$prog > output${SLURM_ARRAY_TASK_ID}.out
```

- If this is the 3rd job in the job array, then the command on the 3rdline of `job_parameters.txt` will be run
- Remember to copy the output back to your home directory beforedeleting the temporary working directory!

### Example
Here is an example running `SLiM` jobs on the cluster

- SLiM file: `merged_same_site_spatial.slim`
- Python driver: `new_driver.py`
- This runs each SLiM simulation `-nreps` times, parses the   output, and writes the desired results to a csv file that will be copied back to my home directory.
- Text file with commands: `slim_job_params.txt`
- Shell script that I’ll submit to SLURM: `slim_job.sh`
- This is an array of length `7`
- I use the `SLURM_ARRAY_TASK_ID` environmental variable to grab a specific line of my param txt file. Each line will tells Python to modify my SLiM file to simulate a specific promoter.
   - For example, the 2nd array job will run `python new_driver.py -d zpgX -nreps 2 -header`, which simulates a zpgX promoter 2 times and creates a csv file with 2 lines (`slim_result_2.csv`)

```bash {filename="slim_job.sh"}
#! /usr/bin/env bash
## #SBATCH --ntasks=1
## #SBATCH --mem=1000
## #SBATCH --partition=regular
## #SBATCH --job-name=slim_job
## #SBATCH --output=slim_job.out
## #SBATCH --array=1-7

# Run 7 different SLiM jobs in parallel
# The parameters for each array job are set by the text file
# Create and move to working directory for job
WORKDIR=/workdir/$USER/$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p $WORKDIR
cd $WORKDIR

# Copy files over to working directory
BASE_DIR=/home/ikk23## cp $BASE_DIR/example/slim_files/merged_same_site_spatial.slim .
cp $BASE_DIR/example/slim_files/new_driver.py .
cp $BASE_DIR/example/slim_files/slimutil.py .
cp $BASE_DIR/example/slim_files/slim_job_params.txt .

# Include SLiM in the path
PATH=$PATH:/home/ikk23/SLiM/SLiM_build
export PATH

# Run program and copy results back to my directory
prog=`sed -n "${SLURM_ARRAY_TASK_ID}p" slim_job_params.txt`
$prog > slim_result_${SLURM_ARRAY_TASK_ID}.csv
cp slim_result_${SLURM_ARRAY_TASK_ID}.csv $BASE_DIR/example/results/

# Clean up working directory
rm -r $WORKDIR
```