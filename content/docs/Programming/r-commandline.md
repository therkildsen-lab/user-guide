---
title: R command line scripts
type: docs
sidebar:
  open: true
---

Most of the time, you'll probably be using R in an interactive session via RStudio/Positron/VScode/Jupyter/etc.
In situations where you have a useful piece of code that can be reused, you can also turn your R script
into an command line program with inputs. We'll go through the simplest form of that process here.

## the goal
Let's say we wanted to create a program called `estimateHET` that took a VCF file as input. We want the program to have an interface like this:

```bash
estimateHET threads vcffile
```

For the sake of this guide, we won't actually be calculating or multithreading anything, but let's pretend this is what our goal is.

## the R code
### shebang
To make your R script executable, you'll first need to declare the proper _shebang_ at the top of the file to let your computer know that this script
needs the R interpreter for execution.

```r {filename="first line of the script"}
#! /usr/bin/env Rscript
```

### setup command line arguments
The simplest way to configure the script to accept command line arguments is with positional arguments. If you aren't familiar, positional arguments
don't have user-facing names or flags, they are just specified by their placement after the program name in the command. Given our intent is to have
the program take the form `estimateHET threads vcffile`, `threads` would be the first positional argument and `vcffile` would be the second positional
argument. We accomplish this using `commandArgs()`

```r {filename="set up command arguments"}
#! /usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
```

What this does is create a variable `args` that will become a list of whatever positional arguments we give our program. The `args` variable will
be indexed numerically to get the values of the positional arguments. In other words, `args[1]` would be the first positional argument, `args[2]`
would be the second positional argument, etc. We can optionally separate these into their own variables to make it easier to work with the values.

```r {filename="optionally split arguments"}
#! /usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
threads <- args[1]
vcf <- args[2]
```

This is also where you would want to include any checks for the arguments, like enforcing that there are exactly 2, making sure `threads` is
an integer, that `vcf` exists, etc.

### load libraries
If your script requires any packages/libraries to run, add them _after_ the `commandArgs()`. This is a personal preference, but it makes
more sense to first check your inputs before loading any libraries.

```r {filename="load libraries"}
#! /usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
threads <- args[1]
vcf <- args[2]

library(dplyr)
library(ggplot2)
```

### write code as usual
After this initial setup, you can use `threads` and `vcf` as normal and write out as simple or as complicated of a script
as required. If you need to create plots, you will probably want to use `png()` or `ggsave()` to have the script take care of
saving the plots. You can likewise write any tables/text/etc. to files as you would usually do. In all, our `estimateHET` script will look
like:

```r {filename="final script"}
#! /usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
threads <- args[1]
vcf <- args[2]

# input checks and docstring

# load any libraries
library(...)

# do stuff here...
```

## make executable
After you've made your script, make sure it's executable using `chmod`:

```bash {filename="make it executable"}
chmod +x estimateHET
```

You can optionally add it to your PATH to call it like a system program. In this example,
we're adding it to  `~/.local/bin`, which is a great place to make a local
PATH. If the folder doesn't exist, you can create it, just make sure to add that folder to
your PATH in your `~/.bashrc` or `~/.zshrc` file.

```bash {filename="add it to your PATH"}
mkdir -p ~/.local/bin
cp ./estimateHET ~/.local/bin
```
