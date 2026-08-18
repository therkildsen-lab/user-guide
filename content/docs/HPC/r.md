---
title: Using R on the server
type: docs
sidebar:
  open: true
---

The instructions on this page are specific to doing things on the server, not your local machine.

## Running RStudio on the server
1.  Run this command to start RStudio server
```bash
/programs/rstudio_server/rstudio_start
```

2.  From a browser on your laptop/desktop computer, go to <http://cbsunt246.biohpc.cornell.edu:8015>
  - Sometimes, you might need to reshresh the page once. Log in using your biohpc username and password

3. If you want to stop the RStudio Server, using this command:
```bash
/programs/rstudio_server/rstudio_stop
```

## Avoid re-plotting figures when knitting an Rmd
You can set `eval=F` in the code block, run it manually, and save the figure to a file. Then, you can start a new code block, set `eval=T`, and use `include_graphics("path_to_the_figure")` to show the figure. Note that if you are knitting to a GitHub formatted md file, the figure needs to be pushed to GitHub as well for it to show up on the GitHub site.

## Using Positron on the server
[Positron](https://positron.posit.co/) is an data science IDE developed by Posit, the developers of RStudio. It's designed to be the successor to the RStudio software by being a flexible, user-friendly workspace. For more info, check out [this](https://www.youtube.com/watch?v=8uRcB34Hhsw) video for a full breakdown of Positron's features. Positron is effectively a reskinned version of Visual Studio Code but with some extra R-specific features, such as customizable plotting and the ability to see all environment variables and dataframes. Beyond R, Positron also supports Python interpreters and has a seamless GitHub integration. Like VS Code, Positron features a marketplace of useful extensions for a variety of tasks. 

Positron is currently in beta, meaning that some features remain in-progress or missing and you may run into bugs. However, you can still install it via its GitHub [Releases](https://github.com/posit-dev/positron/releases) page. To get it working on our server, you will first need to go into the Settings (File > Preferences > Settings) and search for `Kallichore`, and check `Kallichore Supervisor: Enable`. You will then need to connect via `ssh` by hitting `Ctrl + Shift + P` on your keyboard and typing in `Remote-SSH: Connect to Host`. You will be prompted to enter your ssh host address, which should be `yournetid@cbsunt246.biohpc.cornell.edu`. A new window should open, and you will need to enter your BioHPC password. You can then select your working directory by going to the Explorer panel and selecting `Open Folder` and pointing to your desired working directory. 

For more information on customizing Positron, check out this [link](https://www.andrewheiss.com/blog/2024/07/08/fun-with-positron/), which is a bit outdated but contains some useful info on settings and extensions you can implement for a good experience. 