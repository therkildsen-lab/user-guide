SLURM tutorial
================

-   [Resources](#resources)
-   [Cluster structure](#cluster-structure)
    -   [Login nodes](#login-nodes)
    -   [Computing nodes](#computing-nodes)
    -   [Storage servers](#storage-servers)
    -   [Home directory](#home-directory)
-   [Cluster partitions](#cluster-partitions)
-   [Key rules](#key-rules)
-   [Simple example](#simple-example)
-   [Job arrays](#job-arrays)
    -   [Example - running SLiM jobs on the cluster](#example---running-slim-jobs-on-the-cluster)
    -   [Remaining Questions](#remaining-questions)

### Resources

-   [BSCB cluster guide](https://biohpc.cornell.edu/lab/cbsubscb_SLURM.htm)
-   [Slurm introduction by Princeton Research Computing](https://researchcomputing.princeton.edu/slurm)
-   [Introduction to slurm in the Bioinformatics Workbook](https://bioinformaticsworkbook.org/Appendix/Unix/01_slurm-basics.html#gsc.tab=0)
-   [Slurm overview](https://slurm.schedmd.com/overview.html)
-   [Slurm commands reference sheet](https://slurm.schedmd.com/pdfs/summary.pdf)

### Cluster structure

![](https://www.hpc.iastate.edu/sites/default/files/uploads/HPCHowTo/HPCCluster.JPG)

<br>

##### Login nodes

-   There are three login nodes: `cbsulogin`, `cbsulogin2`, and `cbsulogin3`.
-   They are used for submitting jobs or requesting interactive sessions.
-   Use `ssh` to connect to login nodes (Cornell VPN is not necessary).
    -   They all have the domain name `cbsulogin.biohpc.cornell.edu`.
    -   E.g. `ssh netid@cbsulogin.biohpc.cornell.edu`
-   Don't use them for computation.

##### Computing nodes

-   Genenral Info
    -   Currently, there are a total of 16 computing nodes, which are named `cbsubscb01`-`cbsubscb15`, and `cbsubscbgpu01`.
    -   Their specs range from 32-56 in physical cores, and 256-512GB in RAM.
    -   You can access these computing nodes from the login node, by
        -   submitting a job using `sbatch`, OR
        -   requesting an interactive session using `salloc`
    -   Each node can also be accessed directly though `ssh`.
        -   You can't run computationally intensive jobs in these sessions.
        -   This is only for tasks such as job submission, file lookup, and monitoring.
-   Local storage on computing nodes
    -   Each computing node has a local permanent storage and each is assigned to a different lab group.
    -   The local storage of each node is located at the directory `/local/storage`.
    -   The local storage of each node can be mounted to any other node using the command `/programs/bin/labutils/mount_server node_name /storage`.
        -   e.g. `/programs/bin/labutils/mount_server cbsubscb04 /storage`
    -   The mounted storage then becomes available under the directory `/fs/node_name/storage`
    -   This mounting step is usually one of the first things we do in a job script so that your input files can be accessed from any of the computing nodes.
-   Scratch storage on computing nodes
    -   Each computing node has a scratch storage, ranging from 1-2TB in capacity.
    -   They are located under `/workdir/` (and `/SSD/` on some nodes).
    -   It is recommended to copy your input files from network mounted storage space to this scratch storage for computing.
    -   The scratch storage is shared by all users, so after you finish your job, make sure to copy your output files to your permanent storage space, and clear the scrach storage space.
    -   Any files that were not removed by users will be removed automatically when the node receives a new job.
    -   Users who have jobs running on the nodes will **not** have their associated files removed from the scratch space.

##### Storage servers

-   There are three storage servers, which together have a capcity of 281TB.
-   They should not be accessed directly.
-   Instead, they are network mounted in all BSCB machines under `/bscb`, in which each lab group has a subfolder.
-   They are not mounted to the `nt246` server yet.

##### Home directory

-   You will always have the same home directory. It is mounted on all CBSU servers.
-   It has limited storage space and should not be used for computing or storage.

### Cluster partitions

| Partition | Job Time Limit | Nodes                           | Slots                    |
|-----------|----------------|---------------------------------|--------------------------|
| short     | 4 hours        | cbsubscb\[01-15\],cbsubscbgpu01 | 1136                     |
| regular   | 24 hours       | cbsubscb\[01-15\],cbsubscbgpu01 | 348                      |
| long7     | 7 days         | cbsubscb\[01-15\]               | 352                      |
| long30    | 30 days        | cbsubscb\[01-15\]               | 416 (limit 270 per user) |
| gpu       | 3 days         | cbsubscbgpu01                   | 32 + 2 GPUs              |

-   Any jobs submitted from the login node will get to a queue.
-   The cluster has five different queues (or partitions), and each as a different time limit (see the table above).
-   The partition to which a job is submitted can be specified by the `--partition` or `-p` option.
-   Generally, the longer the time limit is, the longer you will have to wait in the queue.
-   Note that there are a total of 1136 slots (i.e. number of tasks that can be requested). So all slots are available for jobs submitted to the short partition, and only a subset of them are available for other partitions.

### Key rules

-   Don't do any computing on your login node (if you do, you'll get emails). Do everything in a script that you submit to the cluster.

-   Each job should perform computations in a temporary working directory
-   start by copying all the files you need from your home directory into the temporary directory
-   copy all desired output from the temporary directory to your home directory
-   delete the temporary directory at the end

ex:

``` bash
# Create and move to a working directory for job
WORKDIR=/SSD/$USER/$JOB_ID-$SLURM_ARRAY_TASK_ID
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

## Simple example

`simple_example.sh` merges 365 fasta files into 1.

Job headers:

-   `#SBATCH --time=10:00` : set a time limit of 10 minutes
-   `#SBATCH --partition=short` : use the **short** queue, since this job will take less than 4 hours
-   `#SBATCH --job-name=simple_job` : this is the name that will appear in `squeue`
-   `#SBATCH --output=simple_job.out` : direct error messsages to this file, which will be placed in the working directory from which you submitted the job

Submit this job with: `sbatch simple_example.sh`

-   You can include job headers here instead. For example, I could have omitted the headers above and instead done `sbatch simple_example.sh -t 10:00 -p short -J simple_job -o simple_job.out`
-   Once you submit your job, you'll get a message that includes the job number
-   ex: `Submitted batch job 1844784`

You can view the status of your jobs with: `squeue -u netid`

-   This should look something like: ![](job_status.png)

-   If you'd rather be notified via email at the job start, end, or crash, include headers `#SBATCH --mail-user=email@address.com` and `#SBATCH --mail-type=ALL`

Kill your job with: `scancel jobnumber`

## Job arrays

If you want to run an identical program 10 times, instead of using a for-loop, you can submit the script as a job array. You'd just need to include the header `#SBATCH --array=1-10` at the top.

-   Each array job will get its own unique ID (SLURM\_ARRAY\_TASK\_ID) that you can make use of in your script.

### Example - running SLiM jobs on the cluster

Shell script: `run_slim_zpg.sh`

-   SLiM file: `merged_same_site_spatial.slim`

-   Python driver: `new_driver.py`
-   This runs each SLiM job nreps times, parses the output, and appends the desired results to a big csv

-   Text file with commands: `run_slim_zpg_params.txt`

-   Shell script that I'll submit to SLURM: `run_slim_zpg.sh`
-   This is an array of 20 jobs
-   I use the SLURM\_ARRAY\_TASK\_ID environmental variable to grab a specific line of my param txt file
-   A line such as `python new_driver.py -d zpg -nreps 10` runs SLiM through the python driver 10 times. The `-d zpg` argument is used within the SLiM file to simulate a gene drive with a ZPG promoter
-   I end up with 200 replicates, since here, all lines are the same.

### Remaining Questions

-   Can `nt246` be network mounted to BSCB nodes?
-   Do you have access to the storage servers?
-   Can the storage server be network mounted to `nt246`?
-   How to backup files in permant storage locations?
-   How to run RStudio Server?
