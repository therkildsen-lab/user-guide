---
title: Cluster Structure
type: docs
sidebar:
  open: true
---

### Login nodes

- There are three login nodes: `cbsulogin`, `cbsulogin2`, and`cbsulogin3`.
- They are used for submitting jobs or requesting interactivesessions.
- Use `ssh` to connect to login nodes (Cornell VPN is not necessary).- They all have the domain name `cbsulogin.biohpc.cornell.edu`.- E.g. `ssh netid@cbsulogin.biohpc.cornell.edu`
- Don’t use them for computation.

### Computing nodes

#### General Info

- Currently, there are a total of 18 computing nodes, which are named`cbsubscb01`-`cbsubscb17`, and `cbsubscbgpu01`.
- Their specs range from 32-64 in physical cores, and 256-1003GB inRAM.
- You can access these computing nodes from the login node, bysubmitting a job using `sbatch` OR by requesting an interactivesession using `salloc`
- Each node can also be accessed directly though `ssh`
- You can’t run computationally intensive jobs in these sessions.- This is only for tasks such as job submission, interactive   session request, file lookup, and monitoring.
- Unlike the login nodes, accessing the computing nodes directly willrequire Cornell network connect (i.e. VPN if you are off campus).

#### Local storage

- Each computing node has a local permanent storage and each isassigned to a different lab group.  
- The computing node assigned to the Therkildsen lab for permanentstorage is `cbsubscb16`.  
- The local storage of each node is located at the directory`/local/storage`.  
- The local storage of each node can be mounted to any other nodeusing the command`/programs/bin/labutils/mount_server node_name /storage`.- e.g. `/programs/bin/labutils/mount_server cbsubscb16 /storage`  
- The mounted storage then becomes available under the directory`/fs/node_name/storage/`  
- This mounting step is usually one of the first things we do in a jobscript so that your input files can be accessed from any of thecomputing nodes.

#### Scratch storage

- Each computing node has a scratch storage, ranging from 1-2TB incapacity.  
- They are located under `/workdir/` (and `/SSD/` on some nodes).  
- It is recommended to copy your input files from network mountedstorage space to this scratch storage for computing, espcially forI/O heavy jobs.  
- The scratch storage is shared by all users, so after you finish yourjob, make sure to copy your output files to your permanent storagespace, and clear the scrach storage space.
- Any files that were not removed by users will be removedautomatically when the node receives a new job.
- Users who have jobs running on the nodes will **not** have theirassociated files removed from the scratch space.

#### Storage servers

- There are three storage servers, which together have a capcity of281TB.
- They should not be accessed directly.
- Instead, they are network mounted in all BSCB machines under`/bscb/`, in which each lab group has a subfolder.
- They are not mounted to the `nt246` server yet.

#### Home directory

- You will always have the same home directory. It is mounted on all CBSU servers.
- It has limited storage space and should not be used for computing orstorage.

## Cluster partitions

| Partition | Job Time Limit | Nodes                   | Slots              |
|-----------|----------------|----------------------------------|--------------------------|
| short    | 4 hours      | cbsubscb\[01-15\], cbsubscbgpu01 | 1392              |
| regular  | 24 hours     | cbsubscb\[01-15\], cbsubscbgpu01 | 435               |
| long7    | 7 days      | cbsubscb\[01-15\]           | 437               |
| long30   | 30 days      | cbsubscb\[01-15\]           | 500 (limit 270 per user) |
| gpu     | 3 days      | cbsubscbgpu01              | 32 + 2 GPUs          |

- Any jobs submitted from the login node will get to a queue.
- The cluster has five different queues (or partitions), and each hasa different time limit (see the table above).
- The partition to which a job is submitted can be specified by the`--partition` or `-p` option, with default being the `short`partition.
- Note that there are a total of 1392 slots (i.e. number of tasks thatcan be requested). So all slots are available for jobs submitted tothe `short` partition, and only a subset of them are available forother partitions.
- Please use the following table to determine which partition(s) tosubmit your jobs to:

| Intended job duration | Partition specification         | Slots available |
|-----------------------|-------------------------------------|-----------------|
| up to 4 hours      | `--partition=short`            | 1392        |
| 4 - 24 hours       | `--partition=regular,long7,long30`  | 1372        |
| 24 hours - 7 days    | `--partition=long7,long30`       | 937         |
| 7 days - 30 days    | `--partition=long30`           | 500         |
| GPU, up to 36 hours  | `--partiton=gpu --gres=gpu:tP100:1` | 32          |