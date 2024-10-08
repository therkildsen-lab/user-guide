---
title: A TL;DR to Python
type: docs
sidebar:
  open: true
---

Most of the time, you'll probably be working with R and Bash, but there just might be a situation where
some tools you're interested in are implemented in Python. This page serves to cover some basics about
Python that wouldn't seem intuitive if you're used to R or Bash.

## 0. Command line programs
Python makes it easy to install your scripts as a command line program. More often than not, you'll
be working with something written in Python that you interact with like a familiar command-line program.
If that's the case, great; you won't need to know any Python to do what you need to do. The remainder of 
this page will help cover concepts useful for writing (or reading) Python code.

## 1. installing packages
In R, you install packages inside an R session using `install.packages("package")`. However, in Python,
you install packages **outside** of a Python session. There's a reason why it was designed this way,
but that's not important right now. Typically, you would install Python packages using the command line
with one of its package managers, usually `pip`. There are other managers, like `poetry`, `conda`, `mamba`,
but `pip` is the standard one for basic use. Installing a package would look like:

```bash {filename="this is a shell session, not inside a python session"}
pip install pandas
```

## 2. importing packages
In R, you load libraries using `library(package)`, typically at the top of a script. In python,
it's the same idea, except the syntax is a little different and more flexible. With Python, you
import packages using `import` like so:
```python
import package
```
 You can also selectively import modules from packages:
```python
from pathlib import Path
```
which reads intuitively as  "from the `pathlib` library, import `Path`".
Another thing you can do is alias your import, i.e. give it a different name. You can accomplish that
using the syntax:
```python
import pandas as pd
```
which reads intuitively as "import the `pandas` library and
for the remainder of the script, let's reference `pandas` as `pd`". The aliasing is an awesome feature
to give you fewer keystrokes, but also to avoid namespace clashes when a library you want to import
has a function that would clash with an existing function, like `print`. A simple example would be:
```python
from rich import print as rprint
```
which would import the `print` function from the `rich` library
and alias it as `rprint` so you can be explicit when you are trying to use the `rich` version. It's
a way to have your cake and eat it, worry-free.

## 3. indentation is code
This design choice takes some getting used to, but it's really not so bad. The idea is that indentation
specifies nesting hierarchy, therefore you don't need extra words/symbols to specify the end of a code block.
To demonstrate this, let's compare `if` blocks between R and Python:
```r {filename="R"}
if(x > 3){
    x <- x + 5
} else {
    x <- x - 1
}
```
In the R example above, the `if` statement requires paired parentheses (open and closed) for the logic test,
along with paired curly braces for both `if` and `else` blocks. Conversely, in python, you begin your `if` block
and use indentations to specify nesting:
```python {filename="python"}
if x > 3:
    x += 5
else:
    x -= 1
```
In most languages, indenting is an optional strategy to make code readable and looking clean. In python,
indentation is strictly enforced and part of your code. You can see how much cleaner and simpler the
python example is. If we were to rewrite the `if` block without indentation, the python interprety will
return an error:
```python {filename="python"}
if x > 3:
x += 5
else:
x -= 1
# SyntaxError: invalid syntax
# IndentationError: expected an indented block after 'if' statement on line 1
```

## 4. dot-indexing
Like many other languages, python uses something called dot indexing, which means you can access features
inside an object using a dot `.`. What those features are can vary; sometimes it's a value, sometimes it's
a function (confusing, but we'll get into that). So, let's say we imported `rich` via `import rich`. We can
access submodules in the `rich` package with the dot, like `rich.print()`. This example should be familiar
if you've ever used the `package::function()` syntax in R.

## 5. data classes and dot-indexing 
There are data types like integers, strings, etc. Python also has something called Classes, which are
data types that can have *methods* specific to that class. Another use of the dot is to access
class-specific functions. For example, if you have a string `"calamari"`, that's the string class.
the string class has a series of methods (class-specific functions) that can be accessed by dot-indexing.
One of them is `upper()`, which will capitalize all the letters of the string, and you would use it like this:
```python {filename="dot-indexing the upper method"}
squid = "calamari"
squid.upper()
# CALAMARI
```
Another such method is `split()`, which splits a character string based on a pattern:
```python {filename="dot-indexing the split method"}
squid = "calamari"
squid.split("l")
# ["ca","amari"]
```
This is a notable departure from doing something like `strsplit("l", squid)` that you would be more
familiar with in other languages like R. There still are plenty of functions that are used in the
ways you are already familiar with, such as `length(object)` or `sum([1,2,3,4])`. It takes a little
bit of getting used to the class-method system and does require a bit of cognitive overhead to know
how to access a particular function/method. If you aren't sure, a great go-to would be to try tab-autocompletion
after writing a dot to let the interpreter reveal the options. Here's an example:
```python {filename="dot-indexing autocompletion"}
>>> a = "calamari"
>>> a.<tab>
a.capitalize()    a.isalpha()       a.ljust(          a.rsplit(
a.casefold()      a.isascii()       a.lower()         a.rstrip(
a.center(         a.isdecimal()     a.lstrip(         a.split(
a.count(          a.isdigit()       a.maketrans(      a.splitlines(
a.encode(         a.isidentifier()  a.partition(      a.startswith(
a.endswith(       a.islower()       a.removeprefix(   a.strip(
a.expandtabs(     a.isnumeric()     a.removesuffix(   a.swapcase()
a.find(           a.isprintable()   a.replace(        a.title()
a.format(         a.isspace()       a.rfind(          a.translate(
a.format_map(     a.istitle()       a.rindex(         a.upper()
a.index(          a.isupper()       a.rjust(          a.zfill(
a.isalnum()       a.join(           a.rpartition(  
```

You can also chain the methods together in this way. Chaining the methods would read from left-to-right.
Let's say we had a string that we wanted to first capitalize, then replace certain letters with other
ones, then split on a specific character:

```python {filename="chaining multiple methods"}
>>> a = "calamari"
>>> a.upper().replace("MAR", "LARA").split("A")
# ['C', 'L', 'L', 'R', 'I']
```
This would functionally be "calamari" => upper => replace => split


## 6. indexing starts at 0
Unless you're already familiar with low-level languages like the C family, you're likely used to
iterables being indexed using 1 to the length of the set. In other words, the first element of a
set would be indexed with `1`, the second with `2`, and so on. Python (any many other languages)
start indices with `0` rather than `1`. The reason being that the source code for python (which is C),
uses `0`-based indexing, both of which do so because computer bits are `0` and `1`, starting at `0`.
In fact, all computer-things start at `0`. Many languages (like R) choose to have `1`-based indexing
because it tends to be more human-intuitive, although a lot of people on StackExchange would argue
against that.
