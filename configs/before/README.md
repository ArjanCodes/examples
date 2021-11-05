# Install requirements

Option 1: Create a new Anaconda/Miniconda environment
```shell
conda create -n <choose a name> -f conda.yaml
```

Option 2: Install packages in an existing environment using pip
```shell
pip install -r requirements.txt
```

# Application entry point

```shell
python main.py
```

# Tensorboard

To start Tensorboard:
```shell
tensorboard --logdir runs
```

The output will be something like:
```shell
TensorBoard 2.6.0 at http://localhost:6006/ (Press CTRL+C to quit)
```

Follow the instructions printed to the terminal to view Tensorboard in a browser.
