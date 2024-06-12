---
title: other info
type: docs
sidebar:
  open: true
---


> source: Q&A with Robert Bukowski

1.  Some of our jobs involve a lot of large files and copying these overto a scratch directory would take a long time. Is this alwaysnecessary in SLURM scripts, or is it ever okay to compute directlyon the mounted storage? What is the best strategy when there are alot of large input files?
  - It’s usually best to just copy all the files over to a scratchdirectory. If you have hundreds of GBs to transfer, this willprobably take 30 mins to an hour.
  - Some exceptions:- If you only need to read a file into memory once, it might be   okay to just work directly off the mounted server. (If the mount   ends up hanging, this will likely only harm *your* job).- You never need to copy **program files** over. You can mount   `cbsunt246` and call programs stored there as per usual.- You can request to use our `cbsubscb16` machine for the job   using the header: `--nodelist=cbsubscb16`. Then you can access   all files in `cbsubscb16` directory without needing to copy   files. However, your job might take a long time to start if no   nodes on `cbsubscb16` are available.

2.  Should we use `scp` or `rsync` instead of mounting `cbsunt246` andcopying files from there?
  - `scp` is preferrable, since mounting the server requires an extralayer of computation.
  - `rsync` is also fine- ex usage: `scp cbsubscb16:/local/storage/path-to-file $DIR`
  - You *will* need to enter a password (which could mess up SLURMscripts). To avoid this, create a passwordless ssh (followdirections in the[guide](https://biohpc.cornell.edu/lab/cbsubscb_SLURM.htm))

3.  How is job priority determined? Can we get an overview of serverusage per lab every once in a while?
  - Usage is calculated from number of CPUs and computing time
  - You are first ranked by lab and then by user within each lab
  - Usage reports are generated every Monday; Robert can send them tomembers or PIs who are interested.

4.  Do we need to specify `--account=nt246_0001` each time we submit ajob for a Therkildsen lab project if our account is under more thanone lab group?
  - Everyone has a “default” lab group. (Robert can give you this infoif you request it).
  - To prevent slowing down/flagging the wrong account, specify theaccount in the header
5.  How do you suggest figuring out the time and memory requirements forSLURM scripts?
  - It’s mostly trial and error, as stated in the guide.
  - Most programs state how their memory requirements scale with thesize of the data in the user manual.
  - There’s currently no BioHPC database on job requirements

6.  What’s your advice on backing up files?
  - If you can’t generate the data within a week of computation, back itup.
  - Always keep 2 copies.
  - Both `cbsunt246` and `cbsubscb16` are rate 6 (everything will befine if 2 discs fail).- They monitor discs, so they usually know when one is “on the   edge”- Backup through biohpc and nt246 are equal in price and efficacy

7.  How can we use RStudio on the cluster without cheating the system?
  - Run RStudio from an interactive session. [Seedirections](https://biohpc.cornell.edu/lab/userguide.aspx?a=software&i=266#c)

```bash
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
  - SCREEN is a persistent session; it will keep running even if you logoff or exit the interactive job. (You cancel SCREEN using`scancel JOBID`, like you would for a SLURM script). It terminatesonce your time or memory limits are reached.
  - `salloc` will terminate any programs you’re running as soon as youlog off or exit

9.  We have a lot of scripts written for the stand-alone server. Isthere a best strategy to make these cluster-compatible?
  - This shouldn’t be too difficult. You need to remember to:1.  Adjust paths (ex: prefix with `/fs/`)2.  Add SLURM headers (or remember to submit the script with the   desired job options)3.  Call programs using their [software   paths](https://biohpc.cornell.edu/lab/labsoftware.aspx), or   alternatively, mount the `cbsunt246` server and use our own copy

10. What if occasionally we produce more tmp files than 246GB in thescratch space? Will tmp files be deleted?
  - No, nothing should be removed while the script is running.
  - Theoretically, tmp file production shouldn’t be limited, providedthat time and memory requirements set by the job are not reached.
  - That being said the scratch space is memory limited. It should beable to handle several hundred GB files at once, but if others areusing the same scratch space, you might have problems.
  - SLURM does not have a way to limit disc access. i.e. there’s no wayto control different jobs access to scratch space

11. What are the best times/dates to submit jobs to the cluster?
  - Varies by day, but things tend to get busy with the grant cycle.
  - Use `squeue` or `slurm_stat.pl` to get usage information, or`squeue_l` for even more information

12. Can we use the scratch space shared by all groups?
  - This is up to the other PIs, but it’s mostly full already.

13. Other information?
  - Don’t ever submit a job from a directory that is not available from*all* machines.- Home directories are always mounted- You can specify the directory you want the job to start in with   the header: `--chdir=/home/bukowski/slurm`
  - Some applications, such as `x11` and `Docker deamon`, are tricky andoperate outside of SLURM
  - The number of nodes has to be specified (with `-N 1`). There is nodefault. Make sure to specify every time.
  - If your job isn’t running, do some debugging on your own beforecontacting them.
