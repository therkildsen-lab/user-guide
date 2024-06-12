---
title: SLURM Resources
type: docs
sidebar:
  open: true
---

The BioHPC uses the SLURM scheduler for job submissions. What this means is that there's an extra layer of abstraction on top of the code you want to run to configure the "job" with resource specifications like time, memory, CPUs, GPUs, etc.

## Computing
### General rules
- Don’t do any computing directly on the login nodes or computingnodes (if you do, you’ll get angry emails).- Instead, either write everything in a script that you submit   using `sbatch`, or request an interactive session using   `salloc`.
- It is also not recommended to do computing directly (i.e. read orwrite) with files that are network-mounted (i.e. `/fs/`, `/bscb/`,`/home/`), especially for jobs that are heavy in I/O.- Instead, start by creating a temporary directory under   `/workdir/` or `/SSD/` (if present).- Then, copy all the files you will need from the network mounted   storage space into the temporary directory.- Perform computation with files in the temporary directory.- Copy all desired output from the temporary directory back to   your network mounted storage space.- Delete the temporary directory at the end.- Below is an example of this workflow.

```bash
# Create and move to a working directory for job
WORKDIR=/workdir/$USER/$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p $WORKDIR
cd $WORKDIR

# Copy files to working directory
BASE_DIR=/home/ikk23
cp $BASE_DIR/slim_files/merged_same_site_spatial.slim .
cp $BASE_DIR/python_scripts/new_driver.py .

# Run program
python new_driver.py > ${SLURM_ARRAY_TASK_ID}.part

# Copy files back to home directory
cp ${SLURM_ARRAY_TASK_ID}.part $BASE_DIR/zpg_output

# Clean up working directory
rm -r $WORKDIR
```
*Note that `/workdir/` is mounted locally to the machine assigned to the job, meaning that `/workdir/` on `cbsuwrkst2` is not accessible from `cbsuwrkst3`.  

### Networked storage via `/home2/`

An alternative to using local storage is to use networked storage in `/home2/`. Like your individual `/home` directory, `/home2/` is accessible across all BioHPC machines and is designed for high-throughput computing. This means that unlike in `/home/` you may run computationally intensive programs in your individual `/home2/` directory.

#### Permissions
`/home2/` has the same permissions as `/home/` and is assigned under your Cornell netid as `/home2/{Your NETID}/`. Technically, members of our lab all have our networked storage directories (`/home/` and `/home2/`) under the `nt246_0001` storage group, meaning the full path is `/home/nt246_0001/{Your NETID}` or `/home2/nt246_0001/{Your NETID}` but they can still be accessed from `/home/{Your NETID}` as they are symlinked.

#### Advantages
An advantage of using `/home2/` is that files no longer need to be copied into local storage, eliminating the need to include a potentially time-consuming copy step in parallelized array jobs as all nodes have access to `/home2/` directly. This includes `cbsunt246`, meaning that you could simultaneously compute on the BioHPC cluster and on the lab server on files in `/home2/`. 

This may be useful on `nt246` for computing on files stored in `cbsubscb16`. Instead of computing using the `/fs/` mount (i.e. `/fs/cbsubscb16/storage/{Your project dir}`) copy your input files to `/home2/`, perform computation, and then copy the outputs back to your project directory.

#### How to use it
For jobs on the HPC cluster using input files hosted on `cbsunt246` or `cbsubscb16`, an effective strategy would be to copy the relevant files into a project directory in `/home2/`, adjust your scripts to use the `/home2/` directory as input, and then copy the outputs to `nt246` or `cbsubscb16` for long-term storage after computing has finished. If your input files will be needed for additional computation in the immediate future, you can keep them on `/home2/` and proceed with your workflow. If not, it is recommended you clear large files/folders from your `/home2/` directory to avoid unnecessarily using up the lab's storage credit balance (see below). 

#### Storage considerations
An important consideration is that each individual is only allocated 200G of networked storage for free and this is pooled across all group members. Storage usage is calculated in TB/years, meaning that short periods of high usage may be OK depending on the runtime of the programs/analyses you are doing. Storage thresholds are "soft" meaning that instead of preventing data transfers when the quota is exceeded BioHPC will simply charge the group for additional storage. 

Additional storage can be bought for ~$100 for 1TB/year, so if you are planning on using `/home2/` for extensive computation with large files it is recommended you purchase additional storage as needed for your project. These credits apply across all lab members so it may be important to coordinate if multiple lab members are planning to use `/home2/` for computation on bulky filesets simultaneously. Current storage usage and the remaining storage credit balance can be viewed in the [My Storage](https://biohpc.cornell.edu//lab/mystorage.aspx) page of the BioHPC website after login.

### Slurm options

Various options can be specified to control the various aspects of
computing on a Slurm cluster. There are two ways to do this:

#### via SBATCH headers

The following example contains the most useful headers. You will need to
delete the text within parentheses if you want to use this as a
template.

```bash {filename="example SLURM headers"}
#!/bin/bash -l             (change the default shell to bash; '-l' ensures your .bashrc will be sourced in, thus setting the login environment)
#SBATCH --nodes=1           (number of nodes, i.e., machines; all non-MPI jobs *must* run on a single node, i.e., '--nodes=1' must be given here)
#SBATCH --ntasks=8          (number of tasks; by default, 1 task=1 slot=1 thread)
#SBATCH --mem=8000          (request 8 GB of memory for this job; default is 1GB per job; here: 8)
#SBATCH --time=1-20:00:00      (wall-time limit for job; here: 1 day and 20 hours)
#SBATCH --partition=long7,long30  (request partition(s) a job can run in; here: long7 and lon30 partition)
#SBATCH --account=bscb09      (project to charge the job to; you should be a member of at least one of 6 projects: ak735_0001,bscb01,bscb02,bscb03,bscb09,bscb10)
#SBATCH --chdir=/home/bukowski/slurm  (start job in specified directory; default is the directory in which sbatch was invoked)
#SBATCH --job-name=jobname         (change name of job)
#SBATCH --output=jobname.out.%j  (write stdout+stderr to this file; %j willbe replaced by job ID)
#SBATCH --mail-user=email@address.com       (set your email address)
#SBATCH --mail-type=ALL       (send email at job start, end or crash - do not use if this is going to generate thousands of e-mails!)
```

When the script is ready, you can save it as `submit.sh`, for example,
and submit it with `sbatch submit.sh`.

Note that this option is only applicable for `sbatch`, but not `salloc`.

#### Appending the options after sbatch or salloc on command
For example
```bash
sbatch --job-name=somename --nodes=1 --ntasks=6 --mem=4000 submit.sh
```
or
```bash
salloc --nodes=1 --ntasks=6 --mem=4000
```

This option works for both `sbatch` and `salloc`. Also, note that the
command line options will override the `#SBATCH` headers, so it might be
a good practice to use the headers as default settings and tweak them
with command line when needed.

#### Other SLURM options
Some other slurm options not specified in above examples include:
- `--nodelist`: computing nodes that you want your jobs to run on.E.g.`--nodelist=cbsubscb12`
- `--exclude`: computing nodes that you **don’t** want your jobs torun on. E.g. `--exclude=cbsubscb10,cbsubscbgpu01`

## Submission example using `sbatch`
In the example below, `simple_example.sh` merges 365 fasta files into 1.

```bash {filename="simple_example.sh"}
#! /usr/bin/env bash
## #SBATCH --time=10:00
## #SBATCH --partition=short
## #SBATCH --job-name=simple_job
## #SBATCH --output=simple_job.out

# Create working directory
WORKDIR=/workdir/$USER/$SLURM_JOB_ID
mkdir -p $WORKDIR## cd $WORKDIR

# Copy files to working directory #
cp /home/ikk23/example/fastas/*.* $WORKDIR## cp /home/ikk23/example/prefix_list.txt $WORKDIR

# Merge files #
COMPILED_FASTA=compiled_sequences.fasta##
touch $COMPILED_FASTA
for PREFIX in `cat prefix_list.txt`; do
    cat $PREFIX'_consensus.fa' >> $COMPILED_FASTA
done

# Transfer back to home directory #
cp $COMPILED_FASTA /home/ikk23/example/results/

# Clean up working directory #
rm -rf $WORKDIR
```

#### Job headers
- `#SBATCH --time=10:00` : set a time limit of 10 minutes
- `#SBATCH --partition=short` : use the **short** queue, since thisjob will take less than 4 hours
- `#SBATCH --job-name=simple_job` : this is the name that will appearin `squeue`
- `#SBATCH --output=simple_job.out` : direct error messsages to thisfile, which will be placed in the working directory from which yousubmitted the job

**Submit this job with**: `sbatch simple_example.sh`

- You can include job headers here instead. For example, I could have omitted the headers above and instead done
```bash
sbatch simple_example.sh -t 10:00 -p short -J simple_job -o simple_job.out
```
- Once you submit your job, you’ll get a message that includes the jobnumber- ex: `Submitted batch job 1844784`

**You can view the status of your jobs with**: `squeue -u netid`

- This should look something like: ![](resources/job_status.png)
- If you’d rather be notified via email at the job start, end, orcrash, include headers 
```
#SBATCH --mail-user=email@address.com` and`#SBATCH --mail-type=ALL
```
**Kill your job with**: `scancel jobnumber`
