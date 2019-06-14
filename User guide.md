# FAQs for using the Therkildsen lab CBSU server

Please add helpful tips to this list!

## Table of Contents

- [Basic server usage](#basics)

  -  [Where can I get more information?](#more_info)
    
  -  [How do I get a CBSU user account?](#account)
    
  -  [How do I access the server from an off-campus location?](#off_campus)
    
  -  [How do I access the server?](#access)
    
  -  [Where do I run programs?](#run_program)
    
  -  [How do I install programs?](#install_program)
    
  -  [How do I check memory usage?](#check_memory)
    
  -  [How do I run programs in the background?](#nohup)
    
  -  [How do I make scripts executable?](#executable)
    
  -  [How do I control the number of threads a program uses?](#thread)
    
  -  [How do I transfer data?](#transfer)
    
  -  [How do I check the disk usage?](#disk_usage)
    
- [Using R on server](#R)

  -  [How to run RStudio on the server?](#rstudio)
    
  -  [How to avoid plotting figures all over again every time when knitting an Rmd file?](#include_graphics)

- [Using GitHub on server](#github)

  - [How can I skip logging in each time that I use GitHub?](#github_login)

<a name="basics"/>

## Basic server usage

<a name="more_info"/>

### Where can I get more information?

Most of the guides below apply to people who purchase hourly credits and don’t have their own physical servers, but there is still some useful information in these links:

CBSU online user guide 
http://cbsu.tc.cornell.edu/lab/userguide.aspx

quick start guide
http://cbsu.tc.cornell.edu/lab/userguide.aspx?a=quickstart

and storage guides 
http://cbsu.tc.cornell.edu/lab/userguide.aspx?a=storage 
http://cbsu.tc.cornell.edu/lab/userguide.aspx?a=storageguide

<a name="account"/>

### How do I get a CBSU user account?

If you have a user account already created, you need to set your password:
https://cbsu.tc.cornell.edu/lab/labpassreset.aspx

Type in your user id (should be the same as your NetID) and click submit. A link to set new password will be sent to your e-mail.

<a name="off_campus"/>

### How do I access the server from an off-campus location?

To access server from off-campus:

1.	Download Cisco AnyConnect Secure Mobility Client

2.	Open program and connect to VPN: cuvpn.cuvpn.cornell.edu

3.	Use your Cornell NetID password when prompted

4.	More info here: https://cbsu.tc.cornell.edu/lab/doc/Remote_access.pdf

<a name="access"/>

### How do I access the server?

Connect to server:

1.	Launch Terminal (Macs only; for PC users see https://cbsu.tc.cornell.edu/lab/doc/Remote_access.pdf)

2.	Type `ssh yournetid@cbsunt246.tc.cornell.edu`

3.	Enter the password you created above

Once logged in, you will be in your network-mounted /home/yournetid/ directory. We also have a shared home directory for the lab with 2TB of backed up storage in `/home/backup/`. This is where we have been backing up important files (fastq and bam files, scripts, etc.) so far. 

<a name="run_program"/>

### Where do I run programs?

All processes (except really tiny jobs) must be done on the local server, /workdir/. To connect to the local server:
`cd /workdir/`

<a name="install_program"/>

### How do I install programs?

There are many programs installed system-wide. A list of software and details on how to use it, see https://cbsu.tc.cornell.edu/lab/labsoftware.aspx. 

You can request installation of software not listed on the CBSU website using the Contact Us link, but installation may take a few days. 

You may also install programs locally yourself. Please always intall new programs under `/workdir/programs/`. You should also keep track of the version number of the program by first creating a new directory with the program name and version number, and install the program in this directory.  

<a name="check_memory"/>

### How do I check memory usage?

Keep an eye on memory and node usage with the command: 

`htop`

A window showing jobs on all 56 nodes and total memory usage will appear. (Be careful not to exceed the 252GB memory, or the server will crash.) Close the window with Control+c. You can also list jobs that are running but aren’t taking up CPU (e.g. crashed jobs) using: 

`ps –ef | grep yournetid`

<a name="nohup"/>

### How do I run programs in the background?

Run commands in the background (i.e. so that you can disconnect and the process will continue running) using nohup. For example, a process normally run with the command:

`program argument1 argument2`

would be run with:

`nohup program argument1 argument2 >& logfile.nohup &`

Output normally printed to the screen would be printed to logfile.nohup.

<a name="executable"/>

### How do I make scripts executable?

If you use shell scripts to run commands, make them executable with
`chmod +x filename`

You can use `chmod` to change permissions on files as well. See `man chmod`.

<a name="thread"/>

### How do I control the number of threads a program uses?

For program that automatically use all available nodes, you can limit the number of nodes used with 

`export OMP_NUM_THREADS=8`

<a name="transfer"/>

### How do I transfer data?

To transfer files between your local computer and the server (good for <1-2 GB files):

1.	Connect to VPN if not on campus

2.	Open a new terminal window or tab (i.e. not a terminal already connected to the server)

3.	Use rsync to transfer data from the server to your computer with the command:

`rsync -av -progress -e ssh yournetid@cbsunt246.tc.cornell.edu:/workdir/Path/To/Your/File.txt /Path/To/Your/Local/Directory/`

4.	to transfer data from your computer to the server, use:

`rsync -av -progress /Path/To/Your/Local/File/ -e ssh yournetid@cbsunt246.tc.cornell.edu:/workdir/Path/To/Your/Directory/`

5.	Use wildcards `*` to sync lots of files, or you can sync a whole directory. Rsync will only sync files that have changed, and won’t re-write ones that haven’t.

If you have lots of files, big files, or need to transfer between two remote servers, use Globus. See https://cbsu.tc.cornell.edu/lab/doc/Globus_at_BioHPC_Lab.pdf

<a name="disk_usage"/>

### How do I check the disk usage?

To check how much space each directory on the /workdir/ is taking up:

`du -sh /workdir/*` 

To check how much free space is left:

`df -h /workdir/`

<a name="R"/>

## Using R on server]

<a name="rstudio"/>

### How to run RStudio on the server?

1. Run this command  to start RStudio server

`/programs/rstudio_server/rstudio_start`

2. From a brower on your laptop/desktop computer, go to 

http://cbsunt246.biohpc.cornell.edu:8015

Sometimes, you might need to reshresh the page once. Log in using your biohpc username and password

3. If you want to stop the RStudio Server, using this command:

`/programs/rstudio_server/rstudio_stop` 

<a name="include_graphics"/>

### How to avoid plotting figures all over again every time when knitting an Rmd file?

You can set `eval=F` in the code block, run it manually, and save the figure to a file. Then, you can start a new code block, set `eval=T`, and use `include_graphics("path_to_the_figure")` to show the figure. Note that if you are knitting to a GitHub formatted md file, the figure needs to be pushed to GitHub as well for it to show up on the GitHub site. 

<a name="github"/>

## Using GitHub on server

<a name="github_login"/>

### How can I skip logging in each time that I use GitHub?

Run `git config --global credential.helper "cache --timeout=3600"`. You can modify the number after `timeout=`. `timeout=3600`, for example, will save your login information for one hour.








