# Automating your Jupyter Notebook as a Website

## Preface
Pavel had this wild idea of tracking his workflow for a project in a Jupyter notebook
(which isn't actually a wild idea). And there are merits to this, because a Jupyter notebook
(hereafter Notebook) is a mix of nicely formatted markdown and executable code cells in most
of the typical languages we might use in bioiformatics. Where they differ from RMarkdown is that
a Notebook is secretly just a very specific kind of JSON file that saves cell outputs into itself,
meaning outputs can be rendered without having to run anything again to see them.

The actual wild idea was that, if that Notebook (or those Notebooks) are already nicely formatted with
descriptive text, code blocks, results, etc., and going into a GitHub repository anyway, why not do a
civic duty to yourself and fellow researchers by building it into a static website
([example](https://pdimens.github.io/haplotagging_simulations/)). We talk a lot about
transparency, etc., and this is a way to actually work towards being better at transparency.

## What you need
- a jupyter notebook with at least one Markdown or code cell
- jupyterbook (only at first)
- a GitHub account

## How to do it
1. Create a GitHub repository to associate with this project and put the Notebook into it
2. Clone at repository locally, usually along the lines of:
```bash
git clone https://github.com/ACCOUNT/REPO_NAME.git
```
3. Open a terminal and navigate to the folder of the repository you just cloned and type:
```bash
jupyter-book init --gh-pages
```
This will create the necessary configs in your local-repo, along with the GitHub Actions workflow to
**automatically build the website** when you push changes to the repository.
4. Open the `myst.yml` file that was just created an fill in the necessary details (if you want)
5. Commit the changes via `git`, `gh`, `VScode`, or whatever method you typically use. If you use `git`, it would look like:
```bash
git add -A
git commit -m "setup jupyterbook configs"
git push
```
6. On the GitHub website, go to the **Settings** tab above your repository and find the **Pages** section at the bottom of the
`Code and Automation` pane on the left side. Under `Build and deployment`, change the `Source` to `GitHub Actions`

That should be the minimum necessary to get you started. With this setup, you will be able to have multiple Notebooks or Markdown
files and Jupyterbook will continue automatically building a website with them.
