---
title: Naming Conventions
type: docs
sidebar:
  open: true
---

# Naming conventions
For sanity and consistency, it's good practice to be intentional with how you name things. Below is the recommended conventions for different kinds of files.

## Github repos
- **Style**: dashes in place of spaces
- **Example**: `this-is-a-kebab-case-name`

## Directories on the server
- **Style**: snake-case (all lowercase with _ in place of spaces)
- **Example**: `this_is_a_snake_case_name`

## Shell scripts
- **Style**: All uppercase for variable names
- **Example**: `WORKDIR=path/to/somewhere`

## R scripts
- **Style**: snake-case for object and function names
- **Example**: `cod_pedigree <- read.table("cod_pedigree.txt")`

## Programs
# Analysis log
Use a github formatted markdown file to keep track of your analysis logs. You can use RMarkdown to generate this markdown file. 

