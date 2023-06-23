# Introduction

JupyterLab is an interactive environment where you can write and execute your Python code.

It can run more than just Python code. It can run *Ju*lia, *Pyt*hon, and *R* (should the be *eR*?) files as well, which is where the name Jupyter comes from.

## JupyterLab advantages
- allows you to immediately visualize your outputs
- allows you to make changes and execute them, seeing the results immediately
- allows you to interweave documentation, commentary, code, and outputs in one place, a practice [Donald Knuth calls "literate programming"](https://en.wikipedia.org/wiki/Literate_programming)

As XKCD points out, that might not be what he says [if you ask Knuth yourself](https://xkcd.com/163/)

## JupyterLab disadvantages
- the notebook carries "state", so subtle bugs can slip in (e.g. using variables that have already been deleted)
  - this is particularly true if you are re-running cells
- the interactivity means you have to be more disciplined with your software engineering. Getting instant results can lead you to getting started faster, but make it more difficult to write tests for code in notebooks.
- the underlying notebook files are JSON notebooks that contain a lot of extra information (such as time the cells were last executed). This makes a lot of the tools we have around code more difficult to apply to notebooks, such as:
	- autoformatters (e.g. black)
	- linters (e.g. pylint)
	- seeing "diffs" between files on github
- it is difficult to import code from notebooks, making them harder to test.

Joel Grus wrote a famous talk, [I don't like notebooks](https://www.youtube.com/watch?v=7jiPeIFXb6U), pointing out many of the cons of notebooks.

# Getting started with notebooks

- Install JupyterLab into your environment, using `pip install jupyterlab`
- Mac and Linux:
  - In your terminal, go to this directory, and type `jupyter lab` 
- Windows
  - (????)

Once JupyterLab opens, you should be able to click on `nb0_getting_started_with_notebooks.ipynb`.

## Once in the notebook

1. You can run each of the cells by pressing Shift-Enter, and experiment by iterating on the code.
2. To run the notebook from top-to-bottom (recommended!), which resets all state, you can go to the menu and select `Kernel > Restart Kernel and Run All`

