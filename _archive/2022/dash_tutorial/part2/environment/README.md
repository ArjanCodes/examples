# Environment Setup

## Installation with Anaconda/Miniconda

Run the two commands from the root directory.

```shell
conda env create -f ./environment/conda.yaml
conda activate dash-app-tutorial
```

## Installation with Pip

**Note:** Python >= 3.9 is required to use the [modern style](https://peps.python.org/pep-0585/) of type annotations.


Run the command from the root directory.

```shell
python -m pip install ./environment/requirements.txt
```