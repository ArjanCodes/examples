NOTE: All of this steps require that you are in the root path, like the following:

`.../examples/2024/tuesday_tips/fail_fast/employee_portal`


  

## Start Server

To start the server run the following command:

Navigate into employee_portal, should look something like the following

```Zsh
poetry run uvicorn main:app --reload
```

## Run PyTest

Create an database:
```Zsh
python ./employee_portal/database/migration.py
```

Seeds with test data
```Zsh
python ./employee_portal/database/seeds.py
```

Run PyTest
```Zsh
pytest
```