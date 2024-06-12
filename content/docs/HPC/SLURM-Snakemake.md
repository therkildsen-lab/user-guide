---
title: Snakemake + SLURM 
type: docs
sidebar:
  open: true
---

# Get Snakemake to submit jobs via SLURM

Snakemake (version 8+) has a fantastic feature of submitting jobs to SLURM (or other schedulers) on your behalf. This feature existed in pervious versions too, but v8 is a complete rewrite of how it works and it's much, **much** simpler than before. This document will walk you through the things you'll need to know to get a Snakemake workflow to automate all of the logistics for working on the BioHPC

## 1. Make sure it's snakemake v8

Snakemake 8 has a much easier cluster submission system, so it'll need to be updated to major version 8, which also requires python version 3.12 to be manually specified

```bash
mamba update -c bioconda -c conda-forge snakemake=8 python=3.12
```

### if you need to install Snakemake

If you don't have Snakemake installed, replace `mamba update` with `mamba install`

```bash
mamba install -c bioconda -c conda-forge snakemake=8 python=3.12
```

### if you aren't in a conda environment

If you aren't in any conda environment whatsoever, replace `mamba update` with `mamba create -n SOMENAME` where `SOMENAME` is the name you want to give your environment. Once created, activate the environment with `mamba activate SOMENAME`.

```bash
mamba create -n snakemake -c bioconda -c conda-forge snakemake=8
mamba activate snakemake
```

### install the plugins

Then, add the SLURM executor plugin and filesystem plugin

```bash
mamba install -c bioconda -c conda-forge snakemake-executor-plugin-slurm snakemake-storage-plugin-fs
```

# 2. Setting up a SLURM profile config

To use the Snakemake SLURM stuff, you'll need a config file, in YAML format, often called a "profile". This file will specify all the necessities of the cluster configuration so that Snakemake can submit jobs on your behalf as governed by the workflow. Create a folder called `profiles` 

```bash
mkdir profiles
```

Within this folder,  create a file named `config.yaml` that looks like this:

```yaml
__use_yte__: true
executor: slurm
default-resources:
  slurm_account: nt246_0001
  slurm_partition: regular
  mem_mb: attempt * 1500
  runtime: 10
jobs: 30
latency-wait: 60
retries: 1
default-storage-provider: fs
local-storage-prefix: /home2/pd348
shared-fs-usage:
  - persistence
  - software-deployment
  - sources
  - source-cache
```

The lines, explained:

### the basic configuration

- `__use_yte__: true` lets Snakemake know to use an enhanced YAML interpreting engine-- don't think too much about it

- `executor: slurm` this tells Snakemake to use that slurm exector plugin you installed earlier, which is configured to work for SLURM schedulers

- `default-resources` is a catch-all group that lets you put in scheduler-specific parameters that don't appear in Snakemake's command line options
  
  - `slurm_account` is the user account that will interact with the SLURM scheduler, which in most cases should be `nt246_0001`
  
  - `slurm_partition` is the name of the BioHPC partition your are requesting, such as `regular` or `long7`. The partition list can be found [here](https://biohpc.cornell.edu/lab/cbsubscb_SLURM.htm).
  
  - `mem_mb` the maximum number of megabytes of memory to request for a given job if not specified in the `resources` directive within a rule
  
  - `jobs` is the maximum number of jobs Snakemake is allowed to submit to SLURM at a given time
  
  - `runtime` is the time (in minutes) requested for the jobs if not specified in the `resources` directive within a rule

- `latency-wait` is the time, in seconds, Snakemake should wait after a job has finished to check if the expected outputs are present

- `retries` is the number of times Snakemake can try to resubmit a failed job. Works best when the Snakemake is setup to change things on retries, like increasing RAM per retry (e.g. `attempt * 1000`), requesting more time from the scheduler, etc. 

### automatic file I/O

This part can be omitted if you don't need snakemake to move files in or out of `home2` (or another directory) between job submissions

- `default-storage-provider` is the type of filesystem to use, where `fs` is a locally mounted filesystem where things are moved (by Snakemake) using `rsync`. Other options can be explored [here](https://snakemake.github.io/snakemake-plugin-catalog/plugins/storage/fs.html#).

- `local-storage-prefix` is a convenient setting to have Snakemake copy inputs to a SCRATCH-type directory, run the job there, then copy the expected outputs back to the project directory upon completion of the job. For the BioHPC, this can be seen as the automated way to move stuff into and out of `home2/USER` without having to think about it all that much.

- `shared-fs-usage` is a list of permissions/specifications for how Snakemake can interact with the filesystem. The options shown in the example above (`persistence`, `software-deployment`, `sources`, and `sources-cache` ) are necessary for Snakemake automating input/output of the `home2` (or other) directory. Unfortunately, the Snakemake documentation on these parameters are lacking, so there isn't more to say about it until that information becomes publicly available.

# 3. Prepare the working directory

At this point, you should have a `profiles/config.yaml` in your working directory. Keep in mind that the folder can be named anything, not specifically `profiles`, but the config file **has** to be named `config.yaml`.

# 4. Run the workflow

How you will invoke Snakemake is specific to your workflow, but a typical invocation of Snakemake could look like this:

```bash
snakemake --cores 15 --sdm conda \
    --workflow-profile profiles \
    --configfile config/config.yaml \
    --snakefile workflow.smk
```

- `--cores` is the number of cores/threads you're allowing the scheduler to use.

- `--workflow-profile` is the relative path to the **directory** with the SLURM configuration you made above, which in this case should just be the folder name `profiles`. 

- `--snakefile` is the path to the workflow snakefile

- `--sdm` [optional] is a shortcut for `--software-deployment-method`, which in this case is telling Snakemake to use the conda configurations written into your workflow to manage runtime software dependencies. Defaults to using mamba. This could also be omitted if there are no `conda` directives inside any rules, or `--sdm apptainer` if the `container` directive is featured inside any rules. 
