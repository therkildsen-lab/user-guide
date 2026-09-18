---
title: Convenience Scripts
type: docs
sidebar:
  open: true
---

It's common that you'll find yourself using a particular script again and again in various 
contexts. If such is the case, it would be useful to be able to call those scripts repeatedly
from your PATH instead of specifying (and remembering) their location each time. To do that,
you just need to create a folder and make sure it's exported in your PATH.

## Creating a script folder
### Create the folder
The location of this folder is usually most convenient in the home directory of your user 
account (`~`) on the server (`/home/netid/`, where `netid` is your netID). This folder can take 
whatever name you like, but we recommend `~/bin` or `~/scripts`. Or if you want it kind of tucked away, it can be in a hidden folder like `~/.local/bin`.
```bash
mkdir ~/scripts
```
### Add it to your PATH
The PATH (all caps) is a special group of places visible to your macOS/Linux system at any
time and where programs are preferentially invoked from. If you call `samtools` without 
specifying an exact path for it, it's most likely being invoked from a folder in the PATH.
POSIX systems like the HPC already have several locations associated with the PATH, and you
can add more on a per-user basis. To do that, you need to modify your `~/.bashrc` or `~/.zshrc`
file, depending on whether you use the bash or zsh shells, respectively. Regardless of which of
these two you use, the instructions are the same:
1. Open `~/.bashrc` or `~/.zshrc` in a terminal editor like `nano` or `vim`
```bash
nano ~/.bashrc
```
2. Towards the top of the config file, add a line with `export PATH=<scriptdir>:$PATH`, where `<scriptdir>` is the path to the directory you made in the previous step (e.g., `~/bin`, `~/.local/scripts`, etc.). The code block below is an _example_ of inserting the `export` statement
into `~/.bashrc`, you can ignore the other lines.
```bash
export PATH=/programs/julia-1.9.3/bin:$PATH
export PATH=~/.local/bin:$PATH       # <- THIS LINE WAS ADDED

alias cp="cp -i"
alias ls="eza --icons"
alias df='df -h'
...
```
3. The next _new_ shell session will incorporate this change. Or, you can force it by asking the shell to reread the config.
```bash
source ~/.bashrc
```

## Useful scripts
This is a non-exhaustive list of scripts that might useful to add to your user account. The
scripts live in this repository under the [scripts/](https://github.com/therkildsen-lab/user-guide/tree/main/scripts) directory.

### disk space by file type
- Name: [totalsize](https://github.com/therkildsen-lab/user-guide/blob/main/scripts/totalsize)
- Purpose: Lets you get the total amount of disk space occupied by files of a given file type in the current directory.
- Dependencies: None
- Usage: Automatically searches recursively in the current directory. Limit recursion depth with optional `<depth>` argument.
  ```bash
  totalsize .ext <depth>
  ```
- Example:
  ```bash
  totalsize .vcf
  ```