# Code headers to include in coding scripts

Scripts of code can get real messy really quickly. The main thing that one can do to keep a script from becoming unuseable once you've forgotten the nitty-gritty of how you set everything up is to make sure you include proper comments within your code.
There has been a lot of great work done on how to properly comment code (e.g. [Microsoft's commenting guidelines](https://docs.microsoft.com/en-us/dotnet/visual-basic/programming-guide/program-structure/comments-in-code), so let's not belabour the point here.

Another nice thing to do is to include a proper header file at the beginning of your code. 
This header file should include any naming schemes being used (e.g. "This script was orginally named ScriptyMcShellFace.sh, and I've renamed this version to BoringName.sh"), as well as the basic purpose of the code, the name of the original author of the script, and the names of any other authors contributing to this script.

Here below is an example header from an R script named `Redund_clean.R` used to generate simulations for a publication, and made publicly avaialble on GitHub:
```
## Originally: redundancy.R
## Katie E Lotterhos
## Feb 12, 2019
## Illustrate concept of genetic redundancy for different phenotypic values
## Mod. by Áki Jarl 
## Added C_chisq calculation with function from Sam Yeaman and visualization
## Aug. 28, 2019
##################################################################################
# Calculate C_chisq and show how it changes with number of loci affecting a trait
##################################################################################
```
