---
title: Naming Conventions
type: docs
sidebar:
  open: true
---

For sanity and consistency, it's good practice to be intentional with how you name things. Below is the recommended conventions for different kinds of files.

**TL;DR:**
| type                      |                                                                    case |
| :------------------------ | ----------------------------------------------------------------------: |
| GitHub repos              |                                       kebab (dashes in place of spaces) |
| Directories on the server |                   snake-case (all lowercase with \_ in place of spaces) |
| Shell scripts             | all uppercase for variable names, snake-case for almost everything else |
| R scripts                 |                                snake-case for object and function names |
| Others                    |                                   snake-case for almost everything else |

{{< details title="Spelling Cases: a review" closed="true" >}}

![](https://pbs.twimg.com/media/ELuERYrU0AAI_7b?format=jpg&name=4096x4096)
{{< /details >}}

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
### Analysis log
Use a github formatted markdown file to keep track of your analysis logs. You can use RMarkdown to generate this markdown file. 


## Other good practices
- <https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745>
- <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510>