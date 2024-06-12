---
title: Background Jobs
type: docs
sidebar:
  open: true
---

# Running things in the background
If you run things interactively (e.g. calling a program directly, running a script), disconnecting from your terminal session
will prematurely terminate the program/script. Why would you disconnect?
- accidentally close the terminal window
- computer shuts off unexpectedly
- internet outtage
So, there are best-practices to make sure that programs will continue to run in the event of unexpected disconnections.

## with nohup
- Run commands in the background (i.e. so that you can disconnect and the process will continue running) using `nohup`. For example, a process normally run with the command:
```bash
program argument1 argument2
```
would be run with:
```bash
nohup program argument1 argument2 >& logfile.nohup &
```
Output normally printed to the screen would be printed to `logfile.nohup`.

## with `screen` or `tmux`
An alternative is to use either `screen` or `tmux`, which are virtual emulators. These are persistent virtual sessions that can
be entered/exited at will and wont terminate programs when you step out of it or get disconnected from it. For simplicity, we'll just cover `screen`:
```bash {filename="create a screen"}
screen -S NAME_OF_SCREEN
```
where `NAME_OF_SCREEN` is whatever descriptive name you want, like `variantcall` etc. It will create
a fresh terminal session onscreen (all existing terminal text will vanish) using your account's default
login shell (BASH, likely). After that, activate any conda/mamba/etc environments if needed and run
programs as you normally would. At any point, you can press `CTRL + a` then `d` (`+` being "and",
not the actual `+` key). This will "detatch" the screen session. You can reattach the screen using
```bash {filename="reattach a screen"}
screen -r NAME_OF_SCREEN
```