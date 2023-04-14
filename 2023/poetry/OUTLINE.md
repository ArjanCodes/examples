## Overview

- If you’ve been writing Python for a while, you probably had to deal with resolving conflicts between different packages and versions. That’s what we call dependency hell.
- Most ecosystems have this problem: you have all sorts of libraries and packages that everybody uses, but there are also different version of the programming language, operating systems, and so on.
- To solve this, you need a separate and isolated environment that you have full control over and that’s easily reproducible in a variety of contexts. That’s what we call a virtual environment.
  - You can create an isolated, lightweight Python environment
  - You can install packages without conflicting with global packages or interfering with other projects
  - You can use different versions of packages and even Python interpreters in different projects.
  - You can easily deploy and replicate the exact dependencies of a project.
- Today I’ll show you what I think is the easiest way to do this, using a tool called Poetry.
- Before you start a new project, it’s important to think about how to set it up and how to organize things in terms of design. I have a free guide that helps you with this. You can get it at arjan.codes/designguide. It contains the 7 steps I take whenever I design a new piece of software, and I hope it helps you avoid some of the mistakes I made in the past. So, arjan.codes/designguide - the link is also in the description.

## Tools

- **_venv:_** included in the Python Standard Library as of Python 3.3 and provides a simple way to create and manage virtual environments. It doesn’t offer any dependency management, being used together with ****\*****pip****\***** to deal with this problem.
- **_virtualenv:_** a third-party tool that allows you to create isolated Python environments. It was one of the first tools available for creating virtual environments. Since Python 3.3, a subset of it has been integrated into the standard library under the [venv module](https://docs.python.org/3/library/venv.html)
- **_pyenv:_** a tool for managing multiple Python versions on a single system. It allows you to switch between different versions of Python and manage virtual environments for each version, a feature not covered by the built-in ****\*\*\*\*****venv****\*\*\*\***** module.
- **_pipenv:_** aims to bring the combination of features from pip, virtualenv, and pyenv and provides a single, unified interface for managing dependencies and virtual environments.
- **_conda:_** conda is a popular open-source package management and environment management system for data science and scientific computing. It provides a way to manage dependencies and virtual environments, and can also manage non-Python packages.
- **_poetry:_** It provides a single, easy and unified interface for managing dependencies, virtual environments, and building and publishing packages. Building and publishing packages are not covered by any other tools mentioned here. Though you can use the built-in setuptools package for this, I’ve shown how this works in a previous video (insert video link)

## What are virtual environments?

- **********\*\*\*\***********It’s a folder structure and also an isolated Python installation in that folder**********\*\*\*\***********
  - When a virtual environment is created, Python executable files are copied or symlinked into that folder structure
  - The folder structure includes:
    - A copy or symlink of the Python binary
    - A pyvenv.cfg file
    - A site-packages directory
  - Lightweight, isolated environment to quickly create and discard when not needed
  - It reuses Python's built-ins and standard library modules from the base Python installation

## The virtual environment process

- There is a well-defined process to set up virtual environments:
  - Create it
  - Activate it
  - Install packages on it
  - Deactivate it
- The idea is the same, done in different ways by each tool.

### Why poetry?

- Simplicity
  - Poetry provides a simple and straightforward way to manage virtual environments and dependencies, without the need for additional tools or complex configuration.
- Package management
  - It integrates both virtual environment management and package management in a single tool, making it easier to manage dependencies for your projects.
- Package distribution
  - Although not shown in this video, it includes features for building, publishing, and distributing packages, making it a complete solution for managing your Python projects, different from the other packages that don’t support this feature.
- Performance
  - Poetry was designed to be fast and efficient, with a focus on performance. It uses a lock file to ensure that your dependencies are always installed in the same state, improving the reproducibility of your projects.
- User experience:
  - Poetry prioritizes the user experience, with a focus on simplicity, elegance, and consistency. An example is when you install a package, it’s added automatically to the dependencies list, a task that should be done manually if any other mentioned tool was used.

### Creating a virtual environment with poetry

- Starting from an empty folder called _\*\*`my-project`:_

```bash
# Installing poetry, it's an external module.
$ pip install poetry

# Initialize poetry
# This command will prompt some questions and
# at the end, it creates the *pyproject.toml* file.
$ poetry init

# Create the virtual environment
$ poetry install

# Verify where the environment was created (the folder structure)
$ poetry env info -p
```

- By default, poetry creates the folder structure in \**\*\*`{cache-dir}/virtualenvs`, `{*cache-dir}\*` being.
  - **Linux:** `$XDG_CACHE_HOME/pypoetry` or `~/.cache/pypoetry`
  - **Windows:** `%LOCALAPPDATA%\pypoetry`
  - **MacOS:** `~/Library/Caches/pypoetry`
- It’s possible to tell poetry to create the folder structure within the current project folder with the following command: `poetry config virtualenvs.in-project true`

### Activating it

- When you create one with poetry, it will be automatically activated by default.
- It’s possible to activate it manually with `poetry shell` command.
- It’s equivalent to venv’s activation:
  - **Linux/MacOS:** `$ source *<venv>*/bin/activate`
  - **Windows:** `C:\> *<venv>*\Scripts\activate.bat`
- In case you have multiple environments, the command `poetry env list` will list all of them, and also shows the active one

```bash
$ poetry env list
.venv (Activated)
my-project-yEN5c_Ea-py3.10
```

### Installing dependencies on it

- Simply run `poetry add <package-name>` to install it. This will install it on the virtual environment and add the package to the `pyproject.toml` file in order to track the dependencies for further installations.

```bash
$ poetry add aioredis
Using version ^1.3.1 for aioredis

Updating dependencies
Resolving dependencies... (0.2s)

Writing lock file

Package operations: 3 installs, 0 updates, 0 removals

  • Installing async-timeout (3.0.1)
  • Installing hiredis (2.0.0)
  • Installing aioredis (1.3.1)
```

- It’s similar to `pip install <package-name>`, but `pip` won’t add it to `requirements.txt` file automatically. **Perhaps it should!**

### Deactivating it

- To deactivate the virtual environment and exit this new shell type `exit`. To deactivate the virtual environment without leaving the shell use `deactivate`.

### Removing it

- To remove a virtual environment just delete its folder completely.

### Changing to another virtual environment

- In order to change from one virtual environment to another, just:
  - Deactivate the current one.
  - Go to the other project that you’ll work on.
  - Activate the other virtual environment.

### Packaging and publishing using poetry

- It’s quite simple to build and publish packages with poetry.
- Using the **\*\***2023-poetry**\*\*** example, just follow the steps:
  - Navigate to `poetry/app` at **wip** repository and follow the steps below

```bash
# Adds a configuration pointing to the PyPi Test repository
# The URL alias will be just test-pipy
poetry config repositories.test-pypi https://test.pypi.org/legacy/

# get a token from https://test.pypi.org/manage/account/token/

# Adds token to the poetry config
# Notice that *pipy-* from tokens beginning must be included
poetry config pypi-token.test-pypi  *pipy-<rest-of-your-token>

# It's possible to configure those credentials using environments variables
# https://python-poetry.org/docs/repositories/#configuring-credentials
# https://python-poetry.org/docs/configuration/#using-environment-variables*

# Build the package
poetry build

# Publish the package to TestPyPi using the --repository (or shortened -r)
poetry publish -r test-pypi

# It's also possible to build the package before publishing it in one command
# in one command with the --build option
poetry publish --build -r test-pypi
```

- [A distribution filename on PyPI consists of a combination of the project name, version number, and distribution type](https://test.pypi.org/help/#file-name-reuse)
- To avoid the \***\*"Filename or contents already exists"\*\*** or \***\*"Filename has been previously used"\*\*** error, make sure to publish it with an increase in versions project at `pyproject.toml` file, otherwise it won’t allow you to publish a package with the same name, version and dist type.

## Considerations

- **Managing dependencies:** You will need to keep track of the packages and versions you have installed in each virtual environment, and make sure they are up-to-date and compatible with each other. Poetry adds the installed package automatically to `pyproject.toml`, but `pip` doesn’t do the same in `requirements.txt`.
- **Switching between environments:** You'll need to activate the correct environment before running your code, which can be a bit of a hassle if you're working on multiple projects that each use different environments. The best suggestion is to create a virtual environment inside each project's root. especially if there are a lot of virtual environments.
- **Compatibility issues:** Some packages may not work properly in a virtual environment, or may require additional setup steps. Examples:
  - `pyautogui` requires the installation of some system-level libraries such as scrot, xdotool, etc. These libraries are not available within the virtual environment, and therefore the package may not work properly or may require additional setup steps to be installed in the virtual environment.
  - packages that use C extensions to achieve better performance. These C extensions may require compilation and link with system-level libraries. The best example is `numpy`.
- **Disk space:** virtual environments can take up a lot of disk space if you have many environments and many packages installed in each of them.

## Common problems

- **Package version conflicts:** If you have multiple virtual environments with different package versions, they may not be compatible with each other and cause errors when you try to run your code.
- **Activation issues:** You might forget to activate the correct virtual environment before running your code, which can lead to errors if the correct packages and dependencies are not available.
- **Missing dependencies**: When you're working on a new project, you may forget to install all the necessary dependencies in the virtual environment, leading to `ModuleNotFound` exceptions.
- **Incorrectly pointing to the virtual environment:** If the environment path is not set correctly or the environment is not activated properly, your code may not be able to access the packages and dependencies in the virtual environment.
