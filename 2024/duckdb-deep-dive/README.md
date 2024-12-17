# DuckDB Deep Dive



## Generate .csv
To generate a random set of data, create and activate the virtual environment

```zsh
uv venv
```

```zsh
source .venv/bin/activate
```

Then, run the following command:


```zsh
python generate_data.py employees.csv 10000000
```

To generate a dataset of 10 000 000 fake employees. Speed might vary depending on the system.