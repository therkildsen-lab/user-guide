FAQs for using the Therkildsen lab CBSU server
================

## Basic server usage

### Where can I get more information?

Most of the guides below apply to people who purchase hourly credits and
don’t have their own physical servers, but there is still some useful
information in these links:

CBSU online user guide <http://cbsu.tc.cornell.edu/lab/userguide.aspx>

quick start guide
<http://cbsu.tc.cornell.edu/lab/userguide.aspx?a=quickstart>

and storage guides
<http://cbsu.tc.cornell.edu/lab/userguide.aspx?a=storage>
<http://cbsu.tc.cornell.edu/lab/userguide.aspx?a=storageguide>

### How do I get a CBSU user account?

If you have a user account already created, you need to set your
password: <https://cbsu.tc.cornell.edu/lab/labpassreset.aspx>

Type in your user id (should be the same as your NetID) and click
submit. A link to set new password will be sent to your e-mail.

### How do I access the server from an off-campus location?

To access server from off-campus:

1.  Download Cisco AnyConnect Secure Mobility Client

2.  Open program and connect to VPN: cuvpn.cuvpn.cornell.edu

3.  Use your Cornell NetID password when prompted

4.  More info here:
    <https://cbsu.tc.cornell.edu/lab/doc/Remote_access.pdf>

### How do I access the server?

Connect to server:

1.  Launch Terminal (Macs only; for PC users see
    <https://cbsu.tc.cornell.edu/lab/doc/Remote_access.pdf>)

2.  Type `ssh yournetid@cbsunt246.tc.cornell.edu`

3.  Enter the password you created above

Once logged in, you will be in your network-mounted /home/yournetid/
directory. We also have a shared home directory for the lab with 2TB of
backed up storage in `/home/backup/`. This is where we have been backing
up important files (fastq and bam files, scripts, etc.) so far.

### How do I transfer data?

To transfer files between your local computer and the server (good for
\<1-2 GB files):

1.  Connect to VPN if not on campus

2.  Open a new terminal window or tab (i.e. not a terminal already
    connected to the server)

3.  Use rsync to transfer data from the server to your computer with the
    command:

`rsync -av -progress -e ssh
yournetid@cbsunt246.tc.cornell.edu:/workdir/Path/To/Your/File.txt
/Path/To/Your/Local/Directory/`

4.  to transfer data from your computer to the server, use:

`rsync -av -progress /Path/To/Your/Local/File/ -e ssh
yournetid@cbsunt246.tc.cornell.edu:/workdir/Path/To/Your/Directory/`

5.  Use wildcards `*` to sync lots of files, or you can sync a whole
    directory. Rsync will only sync files that have changed, and won’t
    re-write ones that haven’t.

If you have lots of files, big files, or need to transfer between two
remote servers, use Globus. See
<https://cbsu.tc.cornell.edu/lab/doc/Globus_at_BioHPC_Lab.pdf>

You can also use Filezilla. See
<https://biohpc.cornell.edu/lab/doc/UsingFileZilla.pdf>

### How do I check memory usage?

Keep an eye on memory and node usage with the command:

`htop`

A window showing jobs on all 56 nodes and total memory usage will
appear. (Be careful not to exceed the 252GB memory, or the server will
crash.) Close the window with Control+c. You can also list jobs that are
running but aren’t taking up CPU (e.g. crashed jobs) using:

`ps –ef | grep yournetid`

### How do I check the disk usage?

To check how much space each directory on the /workdir/ is taking up:

`du -sh /workdir/*`

To check how much free space is left:

`df -h /workdir/`

## Data backup

### Where should we store the backup files?

For sequencing data and other large files (\>30MB), you should use
`/workdir/backup/`.

For small files such as scripts, markdown files, certain figures, and
others, you can store them under your project directory, which should
also be a GitHub repo. You can then use GitHub to back up these files.

For sample metadata, you should use lab Google Drive to back them up.

### What should be backed up?

1.  Zipped raw fastq files (essential)

2.  Zipped ready to map (adapter trimmed and renamed (demultiplexed if
    applicable) (optional)

3.  Raw bam files (unmapped reads removed, but not filtered for mapping
    quality etc). Only save `.bam` files here, never `.sam`. When we
    have multiple fastq files per individual, map first, then merge bams
    (optional)

4.  Realigned, filtered bam files (following indel re-alignment,
    filtering on mapping quality, removal of duplicates). If there are
    multiple bam files per individual, merge before cleaning,
    esp. before removing duplicates.

5.  Sample lists (needed for keeping track of the bam files) - put on
    Github

6.  SNP lists (lists of called SNP sets used for downstream analysis) -
    put on Github

7.  Major result files used for downstream analysis (e.g. mafs files)
    (optional)

8.  Ones that take a long time to run and that you’ll need to re-use

9.  All scripts used to process the data. There should be one master
    scripts that will run the full analysis pipeline (essential), but
    all intermediate scripts should be saved as well.

### When should files be backed up?

You should back up the raw fastq files and sample metadata as soon as
possible.

You should back up the analysis scripts often while you are working on
them.

You can start backing up the other files as long as moving them do not
interfere with your workflow. Do note that you should avoid reading and
(especially) writing under `/workdir/backup/` as much as possible.

### What should be deleted, and when?

### What are the practices that should be avoided?

Don’t move things around or re-name files unless there is reason to
(it’s ok to do if there is)

Don’t work directly in the backup folder, i.e. don’t have your mapping
program write sam files into the backup folder and then convert. Do that
in your working directory and then move over the bam files to be backed
up.

Don’t store files in multiple places

## Running programs on the server

### Where do I run programs?

All processes (except really tiny jobs) must be done on the local
server, /workdir/. To connect to the local server: `cd /workdir/`

### How do I install programs?

There are many programs installed system-wide. A list of software and
details on how to use it, see
<https://cbsu.tc.cornell.edu/lab/labsoftware.aspx>.

You can request installation of software not listed on the CBSU website
using the Contact Us link, but installation may take a few days.

You may also install programs locally yourself. Please always intall new
programs under `/workdir/programs/`. You should also **keep track of the
version number of the program** by first creating a new directory with
the program name and version number, and install the program in this
directory.

### How do I run programs in the background?

Run commands in the background (i.e. so that you can disconnect and the
process will continue running) using nohup. For example, a process
normally run with the command:

`program argument1 argument2`

would be run with:

`nohup program argument1 argument2 >& logfile.nohup &`

Output normally printed to the screen would be printed to logfile.nohup.

### How do I check job status?

To see the job status of **all** jobs running on the server, use `htop`

To see only the status of jobs that **you** are running, use `ps -aux |
grep user_name`

### How do I kill a job?

Get the job ID using `htop` (this shows all jobs being run; look for the
PIDs matching your username). To see only the job numbers that *you* are
currently running, type `pgrep -u USERNAME`

To kill a specific job, use `kill JOBNUM`

To kill *all* jobs associated with your user name, use `nohup pkill -u
USERNAME`

### How do I make scripts executable?

If you use shell scripts to run commands, make them executable with
`chmod +x filename`

You can use `chmod` to change permissions on files as well. See `man
chmod`.

### How do I control the number of threads a program uses?

For program that automatically use all available nodes, you can limit
the number of nodes used with

`export OMP_NUM_THREADS=8`

### How do I set the priority of a process?

To change the CPU usage of a program or command (i.e., give the process
more or less CPU time than other processes), you can set the priority
using the `nice` command, or `renice` if the process is already running.

  - The priority of a process (`PR` or `PRI`) and its niceness value
    (`NI`) can be seen using `top` or `htop`.  
  - `PR` or `PRI` is the process’s actual priority used by the Linux
    kernel to schedule a task.  
  - `NI` is the niceness value that the user can set to control the
    priority of a process.  
  - `NI` ranges from -20 (highest priority value) to 19 (lowest priority
    value), with a default of 0.  
  - Any user may decrease the priority of a process, but root
    permissions are required to increase priority. By increasing the
    niceness of your process, it will decrease the priority and get less
    amount of CPU compared to processes with lower niceness values.

If you are running some shell script *myscript.sh*, you can start the
process with the niceness value in the command: **`nice -n 10 sh
myscript.sh &`**

To change the niceness value of a running process, use the process ID
and run **`renice -n nice_val -p [pid]`**

To change the niceness values of all processes by a user, run **`renice
-n nice_val -u [user]`**

## Using R on the server

### How to run RStudio on the server?

1.  Run this command to start RStudio server

`/programs/rstudio_server/rstudio_start`

2.  From a browser on your laptop/desktop computer, go to

<http://cbsunt246.biohpc.cornell.edu:8015>

Sometimes, you might need to reshresh the page once. Log in using your
biohpc username and password

3.  If you want to stop the RStudio Server, using this
command:

`/programs/rstudio_server/rstudio_stop`

### How to avoid plotting figures all over again every time when knitting an Rmd file?

You can set `eval=F` in the code block, run it manually, and save the
figure to a file. Then, you can start a new code block, set `eval=T`,
and use `include_graphics("path_to_the_figure")` to show the figure.
Note that if you are knitting to a GitHub formatted md file, the figure
needs to be pushed to GitHub as well for it to show up on the GitHub
site.

## Using GitHub on the server

### What are some basic things I need to know to use GitHub on the server?

Check out this [cheat
sheet](https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf).
It has most of the information that you will need.

### How can I skip logging in each time that I use GitHub?

Run `git config --global credential.helper "cache --timeout=3600"`. You
can modify the number after `timeout=`. `timeout=3600`, for example,
will save your login information for one hour.

## Lab conventions

### How do we name files, directories, objects, functions, and others?

GitHub repos: kebab (dashes in place of spaces)

Directories on the server: snake-case (all lowercase with \_ in place of
spaces)

Shell scripts: all uppercase for variable names, snake-case for almost
everything else

R scripts: snake-case for object and function names

Others: snake-case for almost everything
else

![](https://pbs.twimg.com/media/ELuERYrU0AAI_7b?format=jpg&name=4096x4096)

### How do we keep our analysis logs?

We use a github formatted markdown file to keep track of our analysis
pipeline. You can use Rmd to generate this markdown file.

### What are some good coding practices recommended by the lab?

Please read
<https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745>
and
<https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510>

## Miscellaneous tips

### How do I download files from NCBI’s Short Read Archive (SRA)?

Navigate to the SRA (<https://trace.ncbi.nlm.nih.gov/Traces/sra/>) and
retreive the SRA run accession number: these are coded as
SRR\#\#\#\#\#\#\# e.g., SRR7973881

On the server, navigate to the backup directory (see below) or any
directory where you would like to deposit the files

Use the sra toolkit (installed on the server) to download files

`fastq-dump --split-files --gzip SRR#######`

–split-files splits paired-end reads, do not use this for single-end
reads –gzip zips the read files upon downloading

You need only to enter toe SRA accession as is, the sra toolkit will
connect to NCBI automatically
