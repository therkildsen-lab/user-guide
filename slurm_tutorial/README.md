BSCB Cluster Tutorial
================

-   [Resources](#resources)
-   [Cluster structure](#cluster-structure)
    -   [Login nodes](#login-nodes)
    -   [Computing nodes](#computing-nodes)
        -   [General Info](#general-info)
        -   [Local storage on computing
            nodes](#local-storage-on-computing-nodes)
        -   [Scratch storage on computing
            nodes](#scratch-storage-on-computing-nodes)
    -   [Storage servers](#storage-servers)
    -   [Home directory](#home-directory)
-   [Cluster partitions](#cluster-partitions)
-   [Computing](#computing)
    -   [General rules](#general-rules)
    -   [Slurm submission options](#slurm-submission-options)
    -   [Job monitoring](#job-monitoring)
-   [A simple example of job submission using
    `sbatch`](#a-simple-example-of-job-submission-using-sbatch)
-   [Job arrays](#job-arrays)
    -   [Example - running SLiM jobs on the
        cluster](#example---running-slim-jobs-on-the-cluster)
-   [Accessing files from `cbsunt246` within a script or interactive
    session on the
    cluster](#accessing-files-from-cbsunt246-within-a-script-or-interactive-session-on-the-cluster)
-   [Q & A with Robert Bukowski](#q--a-with-robert-bukowski)

## Resources

-   [BSCB cluster
    guide](https://biohpc.cornell.edu/lab/cbsubscb_SLURM.htm)
-   [Slurm introduction by Princeton Research
    Computing](https://researchcomputing.princeton.edu/slurm)
-   [Introduction to slurm in the Bioinformatics
    Workbook](https://bioinformaticsworkbook.org/Appendix/Unix/01_slurm-basics.html#gsc.tab=0)
-   [Slurm overview](https://slurm.schedmd.com/overview.html)
-   [Slurm commands reference
    sheet](https://slurm.schedmd.com/pdfs/summary.pdf)
-   [Recordings of past BioHPC
    workshops](https://biohpc.cornell.edu/login_bio.aspx?ReturnURL=/lab/medialist.aspx)

## Cluster structure

![](https://www.hpc.iastate.edu/sites/default/files/uploads/HPCHowTo/HPCCluster.JPG)

<br>

#### Login nodes

-   There are three login nodes: `cbsulogin`, `cbsulogin2`, and
    `cbsulogin3`.
-   They are used for submitting jobs or requesting interactive
    sessions.
-   Use `ssh` to connect to login nodes (Cornell VPN is not necessary).
    -   They all have the domain name `cbsulogin.biohpc.cornell.edu`.
    -   E.g. `ssh netid@cbsulogin.biohpc.cornell.edu`
-   Don’t use them for computation.

#### Computing nodes

###### General Info

-   Currently, there are a total of 18 computing nodes, which are named
    `cbsubscb01`-`cbsubscb17`, and `cbsubscbgpu01`.
-   Their specs range from 32-64 in physical cores, and 256-1003GB in
    RAM.
-   You can access these computing nodes from the login node, by
    submitting a job using `sbatch` OR by requesting an interactive
    session using `salloc`
-   Each node can also be accessed directly though `ssh`
-   You can’t run computationally intensive jobs in these sessions.
    -   This is only for tasks such as job submission, interactive
        session request, file lookup, and monitoring.
-   Unlike the login nodes, accessing the computing nodes directly will
    require Cornell network connect (i.e. VPN if you are off campus).

###### Local storage on computing nodes

-   Each computing node has a local permanent storage and each is
    assigned to a different lab group.  
-   The computing node assigned to the Therkildsen lab for permanent
    storage is `cbsubscb16`.  
-   The local storage of each node is located at the directory
    `/local/storage`.  
-   The local storage of each node can be mounted to any other node
    using the command
    `/programs/bin/labutils/mount_server node_name /storage`.
    -   e.g. `/programs/bin/labutils/mount_server cbsubscb16 /storage`  
-   The mounted storage then becomes available under the directory
    `/fs/node_name/storage/`  
-   This mounting step is usually one of the first things we do in a job
    script so that your input files can be accessed from any of the
    computing nodes.

###### Scratch storage on computing nodes

-   Each computing node has a scratch storage, ranging from 1-2TB in
    capacity.  
-   They are located under `/workdir/` (and `/SSD/` on some nodes).  
-   It is recommended to copy your input files from network mounted
    storage space to this scratch storage for computing, espcially for
    I/O heavy jobs.  
-   The scratch storage is shared by all users, so after you finish your
    job, make sure to copy your output files to your permanent storage
    space, and clear the scrach storage space.
-   Any files that were not removed by users will be removed
    automatically when the node receives a new job.
-   Users who have jobs running on the nodes will **not** have their
    associated files removed from the scratch space.

#### Storage servers

-   There are three storage servers, which together have a capcity of
    281TB.
-   They should not be accessed directly.
-   Instead, they are network mounted in all BSCB machines under
    `/bscb/`, in which each lab group has a subfolder.
-   They are not mounted to the `nt246` server yet.

#### Home directory

-   You will always have the same home directory. It is mounted on all
    CBSU servers.
-   It has limited storage space and should not be used for computing or
    storage.

## Cluster partitions

| Partition | Job Time Limit | Nodes                            | Slots                    |
|-----------|----------------|----------------------------------|--------------------------|
| short     | 4 hours        | cbsubscb\[01-15\], cbsubscbgpu01 | 1392                     |
| regular   | 24 hours       | cbsubscb\[01-15\], cbsubscbgpu01 | 435                      |
| long7     | 7 days         | cbsubscb\[01-15\]                | 437                      |
| long30    | 30 days        | cbsubscb\[01-15\]                | 500 (limit 270 per user) |
| gpu       | 3 days         | cbsubscbgpu01                    | 32 + 2 GPUs              |

-   Any jobs submitted from the login node will get to a queue.
-   The cluster has five different queues (or partitions), and each has
    a different time limit (see the table above).
-   The partition to which a job is submitted can be specified by the
    `--partition` or `-p` option, with default being the `short`
    partition.
-   Note that there are a total of 1392 slots (i.e. number of tasks that
    can be requested). So all slots are available for jobs submitted to
    the `short` partition, and only a subset of them are available for
    other partitions.
-   Please use the following table to determine which partition(s) to
    submit your jobs to:

| Intended job duration | Partition specification             | Slots available |
|-----------------------|-------------------------------------|-----------------|
| up to 4 hours         | `--partition=short`                 | 1392            |
| 4 - 24 hours          | `--partition=regular,long7,long30`  | 1372            |
| 24 hours - 7 days     | `--partition=long7,long30`          | 937             |
| 7 days - 30 days      | `--partition=long30`                | 500             |
| GPU, up to 36 hours   | `--partiton=gpu --gres=gpu:tP100:1` | 32              |

## Computing

#### General rules

-   Don’t do any computing directly on the login nodes or computing
    nodes (if you do, you’ll get angry emails).
    -   Instead, either write everything in a script that you submit
        using `sbatch`, or request an interactive session using
        `salloc`.
-   It is also not recommended to do computing directly (i.e. read or
    write) with files that are network-mounted (i.e. `/fs/`, `/bscb/`,
    `/home/`), especially for jobs that are heavy in I/O.
    -   Instead, start by creating a temporary directory under
        `/workdir/` or `/SSD/` (if present).
    -   Then, copy all the files you will need from the network mounted
        storage space into the temporary directory.
    -   Perform computation with files in the temporary directory.
    -   Copy all desired output from the temporary directory back to
        your network mounted storage space.
    -   Delete the temporary directory at the end.
    -   Below is an example of this workflow.

``` bash
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

#### Slurm submission options

Various options can be specified to control the various aspects of
computing on a Slurm cluster. There are two ways to do this:

**1. Through `#SBATCH` headers at the beginning of the shell script.**

The following example contains the most useful headers. You will need to
delete the text within parentheses if you want to use this as a
template.

``` bash
#!/bin/bash -l                   (change the default shell to bash; '-l' ensures your .bashrc will be sourced in, thus setting the login environment)
#SBATCH --nodes=1                (number of nodes, i.e., machines; all non-MPI jobs *must* run on a single node, i.e., '--nodes=1' must be given here)
#SBATCH --ntasks=8               (number of tasks; by default, 1 task=1 slot=1 thread)
#SBATCH --mem=8000               (request 8 GB of memory for this job; default is 1GB per job; here: 8)
#SBATCH --time=1-20:00:00        (wall-time limit for job; here: 1 day and 20 hours)
#SBATCH --partition=long7,long30  (request partition(s) a job can run in; here: long7 and lon30 partition)
#SBATCH --account=bscb09         (project to charge the job to; you should be a member of at least one of 6 projects: ak735_0001,bscb01,bscb02,bscb03,bscb09,bscb10)
#SBATCH --chdir=/home/bukowski/slurm   (start job in specified directory; default is the directory in which sbatch was invoked)
#SBATCH --job-name=jobname             (change name of job)
#SBATCH --output=jobname.out.%j  (write stdout+stderr to this file; %j willbe replaced by job ID)
#SBATCH --mail-user=email@address.com          (set your email address)
#SBATCH --mail-type=ALL          (send email at job start, end or crash - do not use if this is going to generate thousands of e-mails!)
```

When the script is ready, you can save it as `submit.sh`, for example,
and submit it with `sbatch submit.sh`.

Note that this option is only applicable for `sbatch`, but not `salloc`.

**2. By appending the options after `sbatch` or `salloc` on command
line.**

For example,

``` bash
sbatch --job-name=somename --nodes=1 --ntasks=6 --mem=4000 submit.sh
```

or

``` bash
salloc --nodes=1 --ntasks=6 --mem=4000
```

This option works for both `sbatch` and `salloc`. Also, note that the
command line options will override the `#SBATCH` headers, so it might be
a good practice to use the headers as default settings and tweak them
with command line when needed.

Some other slurm options not specified in above exmaples include:

-   `--nodelist`: computing nodes that you want your jobs to run on.
    E.g.`--nodelist=cbsubscb12`
-   `--exclude`: computing nodes that you **don’t** want your jobs to
    run on. E.g. `--exclude=cbsubscb10,cbsubscbgpu01`

#### Job monitoring

-   `sinfo` : report the overall state of the cluster and queues
-   `scontrol show nodes` : report detailed information about the
    cluster nodes, including current usage
-   `scontrol show partitions` : report detailed information about the
    queues (partitions)
-   `squeue` : show jobs running and waiting in queues
-   `squeue -u abc123` : show jobs belonging to user abc123
-   `scancel 1564` : cancel job with jobID 1564. All processes
    associated with the job will be killed
-   `slurm_stat.pl cbsubscb`: summarize current usage of nodes,
    partitions, and slots, and number of jobs per user (run on one of
    the login nodes)
-   `get_slurm_usage.pl`: generate information about average duration,
    CPU, and memory usage of your recent jobs (run the command without
    arguments to see usage) - this may help assess real memory needs of
    your jobs and show whether all requested CPUs are actually used.

## A simple example of job submission using `sbatch`

`simple_example.sh` merges 365 fasta files into 1.

``` bash
cat simple_example.sh
```

    ## #!/bin/bash -l
    ## #SBATCH --time=10:00
    ## #SBATCH --partition=short
    ## #SBATCH --job-name=simple_job
    ## #SBATCH --output=simple_job.out
    ## 
    ## # Create working directory
    ## WORKDIR=/workdir/$USER/$SLURM_JOB_ID
    ## mkdir -p $WORKDIR
    ## cd $WORKDIR
    ## 
    ## # Copy files to working directory
    ## cp /home/ikk23/example/fastas/*.* $WORKDIR
    ## cp /home/ikk23/example/prefix_list.txt $WORKDIR
    ## 
    ## # Merge files
    ## COMPILED_FASTA=compiled_sequences.fasta
    ## touch $COMPILED_FASTA
    ## 
    ## for PREFIX in `cat prefix_list.txt`; do
    ##   cat $PREFIX'_consensus.fa' >> $COMPILED_FASTA
    ## done
    ## 
    ## # Transfer back to home directory
    ## cp $COMPILED_FASTA /home/ikk23/example/results/
    ## 
    ## # Clean up working directory
    ## rm -rf $WORKDIR

Job headers:

-   `#SBATCH --time=10:00` : set a time limit of 10 minutes
-   `#SBATCH --partition=short` : use the **short** queue, since this
    job will take less than 4 hours
-   `#SBATCH --job-name=simple_job` : this is the name that will appear
    in `squeue`
-   `#SBATCH --output=simple_job.out` : direct error messsages to this
    file, which will be placed in the working directory from which you
    submitted the job

Submit this job with: `sbatch simple_example.sh`

-   You can include job headers here instead. For example, I could have
    omitted the headers above and instead done
    `sbatch simple_example.sh -t 10:00 -p short -J simple_job -o simple_job.out`
-   Once you submit your job, you’ll get a message that includes the job
    number
    -   ex: `Submitted batch job 1844784`

You can view the status of your jobs with: `squeue -u netid`

-   This should look something like: ![](job_status.png)

-   If you’d rather be notified via email at the job start, end, or
    crash, include headers `#SBATCH --mail-user=email@address.com` and
    `#SBATCH --mail-type=ALL`

Kill your job with: `scancel jobnumber`

## Job arrays

-   If you want to run an identical program 10 times, instead of using a
    for-loop, you can submit the script as a job array of length 10.
    This is controlled by the header: `#SBATCH --array=1-10`
-   Each array job will get its own unique ID, `SLURM_ARRAY_TASK_ID`,
    that you can make use of in your script.
-   If you want each job in a 1-10 array to run something different, you
    can create a text file with 10 lines and have each line specify the
    command you want to run.
    -   Make sure to copy this text file over to the temporary working
        directory!
    -   In the shell script, write:

``` bash
# go to the <SLURM_ARRAY_TASK_ID> line of the job_parameters.txt file
# and run this command
# for example, this line could read `python my_script.py 4`
prog=`sed -n "${SLURM_ARRAY_TASK_ID}p" job_parameters.txt`
$prog > output${SLURM_ARRAY_TASK_ID}.out
```

-   If this is the 3rd job in the job array, then the command on the 3rd
    line of `job_parameters.txt` will be run
-   Remember to copy the output back to your home directory before
    deleting the temporary working directory!

#### Example - running SLiM jobs on the cluster

-   SLiM file: `merged_same_site_spatial.slim`

-   Python driver: `new_driver.py`

    -   This runs each SLiM simulation `-nreps` times, parses the
        output, and writes the desired results to a csv file that will
        be copied back to my home directory.

-   Text file with commands: `slim_job_params.txt`

-   Shell script that I’ll submit to SLURM: `slim_job.sh`

    -   This is an array of length 7.
    -   I use the SLURM\_ARRAY\_TASK\_ID environmental variable to grab
        a specific line of my param txt file. Each line will tells
        Python to modify my SLiM file to simulate a specific promoter.
        -   For example, the 2nd array job will run
            `python new_driver.py -d zpgX -nreps 2 -header`, which
            simulates a zpgX promoter 2 times and creates a csv file
            with 2 lines (`slim_result_2.csv`)

``` bash
cat slim_job.sh
```

    ## #!/bin/bash -l
    ## #SBATCH --ntasks=1
    ## #SBATCH --mem=1000
    ## #SBATCH --partition=regular
    ## #SBATCH --job-name=slim_job
    ## #SBATCH --output=slim_job.out
    ## #SBATCH --array=1-7
    ## 
    ## # Run 7 different SLiM jobs in parallel.
    ## # The parameters for each array job are set by the text file.
    ## 
    ## # Create and move to working directory for job
    ## WORKDIR=/workdir/$USER/$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID
    ## mkdir -p $WORKDIR
    ## cd $WORKDIR
    ## 
    ## # Copy files over to working directory
    ## BASE_DIR=/home/ikk23
    ## cp $BASE_DIR/example/slim_files/merged_same_site_spatial.slim .
    ## cp $BASE_DIR/example/slim_files/new_driver.py .
    ## cp $BASE_DIR/example/slim_files/slimutil.py .
    ## cp $BASE_DIR/example/slim_files/slim_job_params.txt .
    ## 
    ## # Include SLiM in the path
    ## PATH=$PATH:/home/ikk23/SLiM/SLiM_build
    ## export PATH
    ## 
    ## # Run program and copy results back to my directory
    ## prog=`sed -n "${SLURM_ARRAY_TASK_ID}p" slim_job_params.txt`
    ## $prog > slim_result_${SLURM_ARRAY_TASK_ID}.csv
    ## cp slim_result_${SLURM_ARRAY_TASK_ID}.csv $BASE_DIR/example/results/
    ## 
    ## # Clean up working directory
    ## rm -r $WORKDIR

## Accessing files from `cbsunt246` within a script or interactive session on the cluster

The old `cbsunt246` server has already been mounted onto the new
`cbsubscb16` cluster server. To access any file, just use the prefix
`/fs/cbsunt246` before the rest of the path `/workdir/...`

Ex: accessing a `cbsunt246` file within an `salloc` interactive session

``` bash
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

``` bash
cat trial_job.sh
```

    ## #!/bin/bash -l
    ## #SBATCH --ntasks=1
    ## #SBATCH --mem=1G
    ## #SBATCH --partition=short
    ## #SBATCH --job-name=trial_job
    ## #SBATCH --output=trial_job.txt
    ## 
    ## # Make temporary working directory
    ## USER=ikk23
    ## WORKDIR=/workdir/${USER}/${SLURM_JOB_ID}
    ## mkdir $WORKDIR
    ## 
    ## # Mount the cbsunt246 server
    ## /programs/bin/labutils/mount_server cbsunt246 /workdir
    ## 
    ## # Copy a file from the old server into the scratch directory
    ## cp /fs/cbsunt246/workdir/shad/shad-lcwgs/sample_lists/error_contigs.txt $WORKDIR
    ## 
    ## # Do some computing in the scratch directory: 
    ## # ex here: print the first 2 lines of the file and save it to a new file
    ## cd $WORKDIR
    ## cat error_contigs.txt | awk 'NR==1 || NR==2' > first_two_lines_error_contigs.txt
    ## 
    ## # Copy output to a directory in the old server
    ## cp first_two_lines_error_contigs.txt /fs/cbsunt246/workdir/shad/shad-lcwgs/
    ## 
    ## # Remove the scratch directory
    ## rm -rf $WORKDIR

## Q & A with Robert Bukowski

1.  Some of our jobs involve a lot of large files and copying these over
    to a scratch directory would take a long time. Is this always
    necessary in SLURM scripts, or is it ever okay to compute directly
    on the mounted storage? What is the best strategy when there are a
    lot of large input files?

-   It’s usually best to just copy all the files over to a scratch
    directory. If you have hundreds of GBs to transfer, this will
    probably take 30 mins to an hour.
-   Some exceptions:
    -   If you only need to read a file into memory once, it might be
        okay to just work directly off the mounted server. (If the mount
        ends up hanging, this will likely only harm *your* job).
    -   You never need to copy **program files** over. You can mount
        `cbsunt246` and call programs stored there as per usual.
    -   You can request to use our `cbsubscb16` machine for the job
        using the header: `--nodelist=cbsubscb16`. Then you can access
        all files in `cbsubscb16` directory without needing to copy
        files. However, your job might take a long time to start if no
        nodes on `cbsubscb16` are available.

2.  Should we use `scp` or `rsync` instead of mounting `cbsunt246` and
    copying files from there?

-   `scp` is preferrable, since mounting the server requires an extra
    layer of computation.
-   `rsync` is also fine
    -   ex usage: `scp cbsubscb16:/local/storage/path-to-file $DIR`
-   You *will* need to enter a password (which could mess up SLURM
    scripts). To avoid this, create a passwordless ssh (follow
    directions in the
    [guide](https://biohpc.cornell.edu/lab/cbsubscb_SLURM.htm))

3.  How is job priority determined? Can we get an overview of server
    usage per lab every once in a while?

-   Usage is calculated from number of CPUs and computing time
-   You are first ranked by lab and then by user within each lab
-   Usage reports are generated every Monday; Robert can send them to
    members or PIs who are interested.

4.  Do we need to specify `--account=nt246_0001` each time we submit a
    job for a Therkildsen lab project if our account is under more than
    one lab group?

-   Everyone has a “default” lab group. (Robert can give you this info
    if you request it).
-   To prevent slowing down/flagging the wrong account, specify the
    account in the header.

5.  How do you suggest figuring out the time and memory requirements for
    SLURM scripts?

-   It’s mostly trial and error, as stated in the guide.
-   Most programs state how their memory requirements scale with the
    size of the data in the user manual.
-   There’s currently no BioHPC database on job requirements

6.  What’s your advice on backing up files?

-   If you can’t generate the data within a week of computation, back it
    up.
-   Always keep 2 copies.
-   Both `cbsunt246` and `cbsubscb16` are rate 6 (everything will be
    fine if 2 discs fail).
    -   They monitor discs, so they usually know when one is “on the
        edge”
    -   Backup through biohpc and nt246 are equal in price and efficacy

7.  How can we use RStudio on the cluster without cheating the system?

-   Run RStudio from an interactive session. [See
    directions](https://biohpc.cornell.edu/lab/userguide.aspx?a=software&i=266#c)

ex:

``` bash
ssh ikk23@cbsulogin2.tc.cornell.edu

# request interactive session
salloc --nodes=1 --ntasks=1 --mem=1G --partition=short --time=00:10:00

# go to the server you want to run RStudio from
ssh cbsubscb16

# start RStudio (you might get the message that it's already running)
/programs/rstudio_server/rstudio_start
```

On your browser, log in from:
<http://cbsubscb16.biohpc.cornell.edu:8015>

8.  Is there an advantage of using SCREEN over salloc?

-   SCREEN is a persistent session; it will keep running even if you log
    off or exit the interactive job. (You cancel SCREEN using
    `scancel JOBID`, like you would for a SLURM script). It terminates
    once your time or memory limits are reached.
-   `salloc` will terminate any programs you’re running as soon as you
    log off or exit

9.  We have a lot of scripts written for the stand-alone server. Is
    there a best strategy to make these cluster-compatible?

-   This shouldn’t be too difficult. You need to remember to:
    1.  Adjust paths (ex: prefix with `/fs/`)
    2.  Add SLURM headers (or remember to submit the script with the
        desired job options)
    3.  Call programs using their [software
        paths](https://biohpc.cornell.edu/lab/labsoftware.aspx), or
        alternatively, mount the `cbsunt246` server and use our own copy

10. What if occasionally we produce more tmp files than 246GB in the
    scratch space? Will tmp files be deleted?

-   No, nothing should be removed while the script is running.
-   Theoretically, tmp file production shouldn’t be limited, provided
    that time and memory requirements set by the job are not reached.
-   That being said the scratch space is memory limited. It should be
    able to handle several hundred GB files at once, but if others are
    using the same scratch space, you might have problems.
-   SLURM does not have a way to limit disc access. i.e. there’s no way
    to control different jobs access to scratch space

11. What are the best times/dates to submit jobs to the cluster?

-   Varies by day, but things tend to get busy with the grant cycle.
-   Use `squeue` or `slurm_stat.pl` to get usage information, or
    `squeue_l` for even more information

12. Can we use the scratch space shared by all groups?

-   This is up to the other PIs, but it’s mostly full already.

13. Other information?

-   Don’t ever submit a job from a directory that is not available from
    *all* machines.
    -   Home directories are always mounted
    -   You can specify the directory you want the job to start in with
        the header: `--chdir=/home/bukowski/slurm`
-   Some applications, such as `x11` and `Docker deamon`, are tricky and
    operate outside of SLURM
-   The number of nodes has to be specified (with `-N 1`). There is no
    default. Make sure to specify every time.
-   If your job isn’t running, do some debugging on your own before
    contacting them.
