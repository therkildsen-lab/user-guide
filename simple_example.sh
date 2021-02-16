#!/bin/bash -l
#SBATCH --ntasks=1
#SBATCH --mem=1000
#SBATCH --time=10:00
#SBATCH --partition=short
#SBATCH --job-name=simple_job
#SBATCH --output=simple_job.out

# Create working directory
WORKDIR=/SSD/$USER/$JOB_ID
mkdir -p $WORKDIR
cd $WORKDIR

# Copy files to working directory
cp /home/ikk23/example/fastas/*.* $WORKDIR
cp /home/ikk23/example/prefix_list.txt $WORKDIR

# Merge files
COMPILED_FASTA=compiled_sequences.fasta
touch $COMPILED_FASTA

for PREFIX in `cat prefix_list.txt`; do
  cat $PREFIX'_consensus.fa' >> $COMPILED_FASTA
done

# Transfer back to home directory
cp $COMPILED_FASTA /home/ikk23/example/results/

# Clean up working directory
rm -rf $WORKDIR
