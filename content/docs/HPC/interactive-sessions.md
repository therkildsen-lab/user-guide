---
title: Interactive Sessions
type: docs
sidebar:
  open: true
---

# Accessing files from `cbsunt246` within a script or interactive session on the cluster

The old `cbsunt246` server has already been mounted onto the new
`cbsubscb16` cluster server. To access any file, just use the prefix
`/fs/cbsunt246` before the rest of the path `/workdir/...`

Ex: accessing a `cbsunt246` file within an `salloc` interactive session

```bash
# log into the cluster
ssh ikk23@cbsulogin2.tc.cornell.edu

# request an interactive session
salloc --nodes=1 --ntasks=1 --mem=1G --partition=short --time=00:10:00

# navigate to repo on cbsunt246
cd /fs/cbsunt246/workdir/shad/shad-lcwgs/

# mount server
/programs/bin/labutils/mount_server cbsunt246 /workdir

# do some computation
touch new_file.txt # will be stored on the cbsunt246 server

# exit the interactive job
exit
```

Note: you might get the message that the server has already been
mounted.

Ex: accessing a `cbsunt246` file within a SLURM script.

```bash {filename="trial_job.sh"}
#! /usr/bin/env bash

## #SBATCH --ntasks=1
## #SBATCH --mem=1G
## #SBATCH --partition=short
## #SBATCH --job-name=trial_job
## #SBATCH --output=trial_job.txt

# Make temporary working directory
USER=ikk23
WORKDIR=/workdir/${USER}/${SLURM_JOB_ID}
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
```
