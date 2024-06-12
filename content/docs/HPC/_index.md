---
title: HPC Information
type: docs
sidebar:
  open: true
---

# BSCB Cluster Tutorial
This section is intended to guide you towards submitting jobs to the BioHPC cluster with minimal friction. If you haven't used an HPC before, there will be a bit of a learning curve. However, the concept is simple:
1. You login to one of the nodes on the server
2. You setup a script with instructions for what you want the HPC to run
3. You "submit" your script to the HPC and it adds it to a queue
3. The "scheduler" on the HPC interprets the resources you're requesting (CPUs, memory, time) and will run the script on one of the "compute" nodes when those resources become available 

## Useful Resources
- [BSCB clusterguide](https://biohpc.cornell.edu/lab/cbsubscb_SLURM.htm)
- [Slurm introduction by Princeton ResearchComputing](https://researchcomputing.princeton.edu/slurm)
- [Introduction to slurm in the BioinformaticsWorkbook](https://bioinformaticsworkbook.org/Appendix/Unix/01_slurm-basics.html#gsc.tab=0)
- [Slurm overview](https://slurm.schedmd.com/overview.html)
- [Slurm commands referencesheet](https://slurm.schedmd.com/pdfs/summary.pdf)
- [Recordings of past BioHPCworkshops](https://biohpc.cornell.edu/login_bio.aspx?ReturnURL=/lab/medialist.aspx)

## Cluster structure
![cluster configuration diagram](https://www.hpc.iastate.edu/sites/default/files/uploads/HPCHowTo/HPCCluster.JPG)

### Job monitoring
- `sinfo` : report the overall state of the cluster and queues
- `scontrol show nodes` : report detailed information about thecluster nodes, including current usage
- `scontrol show partitions` : report detailed information about thequeues (partitions)
- `squeue` : show jobs running and waiting in queues
- `squeue -u abc123` : show jobs belonging to user `abc123`
- `scancel 1564` : cancel job with jobID `1564`. All processesassociated with the job will be killed
- `slurm_stat.pl cbsubscb`: summarize current usage of nodes,partitions, and slots, and number of jobs per user (run on one ofthe login nodes)
- `get_slurm_usage.pl`: generate information about average duration,CPU, and memory usage of your recent jobs (run the command withoutarguments to see usage) - this may help assess real memory needs ofyour jobs and show whether all requested CPUs are actually used.


