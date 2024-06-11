#!/bin/bash -l
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --partition=short
#SBATCH --job-name=trial_job
#SBATCH --output=trial_job.txt

# Make temporary working directory
USER=ikk23
WORKDIR=/workdir/${USER}-${SLURM_JOB_ID}
mkdir $WORKDIR

# Mount the cbsunt246 server
/programs/bin/labutils/mount_server cbsunt246 /workdir

# Copy a file from the old server into the scratch directory
cp /fs/cbsunt246/workdir/shad/shad-lcwgs/sample_lists/error_contigs.txt $WORKDIR

# Do some computing in the scratch directory: 
# ex here: print the first 2 lines of the file and save it to a new file
cd $WORKDIR
cat error_contigs.txt | awk 'NR==1 || NR==2' > first_two_lines_error_contigs.txt

# Copy output to a directory in the old server
cp first_two_lines_error_contigs.txt /fs/cbsunt246/workdir/shad/shad-lcwgs/

# Remove the scratch directory
rm -rf $WORKDIR