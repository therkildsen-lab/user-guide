---
title: Jupyter Notebooks as Websites
type: docs
sidebar:
  open: true
---

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
The lab has a [template repository](https://github.com/therkildsen-lab/jupyter-workflow) to set this up pretty seamlessly.
### Option 1 - click a button
On the top-right side of the page you can press the green "Use this template" button to **Create a new repository**
### Option 2 - clone the repo
```bash
git clone https://github.com/therkildsen-lab/jupyter-workflow.git
```

That's it. The repository has already has a GitHub action to build and deploy the site on pushes.

- You can delete the `README.md` file, or rewrite it to better describe the repository.
- You will need to modify the `myst.yml` file that was just created an fill in the necessary details (if you want)
- If not setup, on the GitHub website, go to the **Settings** tab above your repository and find the **Pages** section at the bottom of the
`Code and Automation` pane on the left side. Under `Build and deployment`, change the `Source` to `GitHub Actions`

That should be the minimum necessary to get you started. With this setup, you will be able to have multiple Notebooks or Markdown
files and Jupyterbook will continue automatically building a website with them.
