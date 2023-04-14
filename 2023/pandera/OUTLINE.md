## Overview

- pandas is a fast, powerful, flexible, and easy-to-use open-source data analysis and manipulation tool, built on top of the Python programming language.
- It’s an external dependency, and it should be installed with `pip install pandas`
- There are two main data structures in pandas: `DataFrame` and `Series`
  - `DataFrame` is equivalent to a table with columns and rows
  - `Series` is one column of a `DataFrame`, and basically a pair of key-value for rows and the specific column.
- Pandas `DataFrame` and `Series` make it difficult (with poor definitions) to use type hints properly.
  - defining type hints for a complex dataset, with different columns and data types, is really challenging, eventually impossible, using only pandas
  - For a full specification, please see **[PEP 484](https://peps.python.org/pep-0484/),** and for a simplified introduction to type hints, see **[PEP 483](https://peps.python.org/pep-0483/)**
- This is where pandera comes in handy.
  - pandera is a great data validation tool
  - It allows us to combine the pandera powerful validation checking with type hints to use it correctly and completely, being not too simple as pandas.

## Type hints with pandas

- Can be achieved in the most simple way using `Series` and `DataFrame` basic classes from pandas.

```python
def retrieve_retail_products(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path)
```

- This isn’t enough, since `Series` and `DataFrame` are complex structures requiring much more information than just the type. We may want to know:
  - What columns are in the `DataFrame`?
  - What are the datatypes for each column or in the `Serie`?
  - Are null values allowed on those columns?
  - Is there some threshold upper and lower limits that we are expecting?
- This might lead us to try to define type hints like the below example, but it’s not possible. And even if it were possible, it would only answer the first question above.

```python
def retrieve_retail_products(path: Path | str) -> pd.DataFrame[str, str, float]:
    return pd.read_csv(path)
```

## String-type

- Pandas have two ways to store strings.

1. `object` dtype, which can hold any Python object, including strings.
2. `StringDtype`**,** which is dedicated to strings. Besides this official recommendation, I’ve never seen this in practice at all. Any columns of the string are normally kept as an `object`, or in some cases, as `categorical` using the `CategoricalDtype`

## Arbitrary objects types

- Arbitrary objects may be stored using the `object` dtype but should be avoided to the extent possible (for performance and interoperability with other libraries and methods).

## Pandera validation

- It’s possible to define the complete `DataFrame` schema in a class, just like pydantic, and use it as a type hint.
- It’s possible to define type hints just as a piece of visual information, or you can really check if `DataFrame` is following the defined schema.
- To make a real validation checking using type hints there is a decorator in pandera: `check_types`. Just decorate the function and it will raise an exception if the schema is not compliant with the robust pandera type hint.

## Pandera dtypes

- Pandera has its own implemented dtypes with a well-defined interface for validations.
- They are divided into some logical categories:
  - \***\*Library-agnostic dtypes:\*\*** here, some of the most common data types that are not specific to any framework, are included. Some examples are `pandera.dtypes.Bool`, for representing boolean values; `pandera.dtypes.Int`, for integer values; `pandera.dtypes.String` for the built-in string type, and many others. The complete list can be found [at this link](https://pandera.readthedocs.io/en/stable/reference/dtypes.html#library-agnostic-dtypes).
  - **Specific pandas dtypes:** because pandera has great integration with pandas, some of the native dtypes in pandas were converted to pandera to expand its usability and be part of the pandera API for validations. Some examples: `pandera.engines.pandas_engine.BOOL` for the `pandas.BooleanDtype`; `pandera.engines.pandas_engine.INT64` for `pandas.Int64Dtype`. The complete mapping types from pandas to pandera can be found [here in this other link.](https://pandera.readthedocs.io/en/stable/reference/dtypes.html#pandas-dtypes)
  - ********\*\*\*\*********\*\*********\*\*\*\*********Pydantic dtype:********\*\*\*\*********\*\*********\*\*\*\********* pandera has also introduced a Pydantic-specific dtype to be used for validating rows in a dataframe using the `pandera.engines.pandas_engine.PydanticModel`
- Not only those types above are included in pandera, but also some utility type validation, like `is_numeric`, `is_int`, `is_float` and many others that can be found [at this link](https://pandera.readthedocs.io/en/stable/reference/dtypes.html#utility-functions).

## Pandera integration

- Pandera ships with integrations with other tools in the Python ecosystem like the well-known FastAPI, Mypy and Pydantic.
  - **FastAPI:** It’s possible to use the pandera schema to validate endpoint inputs and outputs using type hints as a defined class that inherits from `pa**.**SchemaModel`. Also, pandera provides a `from_format` schema model configuration option to read a dataframe from a particular serialization format
  - **Mypy:** Pandera integrates with Mypy to provide static type-linting of dataframes, relying on pandas-stubs for typing information.
  - **Pydantic:** pandera `SchemaModel` is fully compatible with [pydantic](https://pydantic-docs.helpmanual.io/). You can specify a `SchemaModel` in a pydantic `BaseModel` as you would any other field. The opposite, defining a `BaseModel` in pydantic from a pandera `SchemaModel` it’s also possible if you are using pandera’s version 0.10.0 it higher
- Other tools for integration are also available: [Hypothesis](https://pandera.readthedocs.io/en/stable/data_synthesis_strategies.html#data-synthesis-strategies) and [Frictionless](https://pandera.readthedocs.io/en/stable/frictionless.html#frictionless-integration). But they aren’t famous as the three ones mentioned above.

## Code examples

- Start with the `pa_validation_type_hints.py` example.
  - Here you can show how to define a custom schema that can be used within type hints.
  - To use this kind of validation, just point to `@pa.check_types(*lazy*=True)` decorator before the `retrieve_retail_products` that have the dataset as an output.
  - But defining the schema can be cumbersome, especially if you have a lot of columns.
- From this point, you can jump to the `pa_validation_schema_inference.py`
  - This script generates automatically the pandera schema used for validation.
  - It will be saved into another script called `infered_schema.py` and the schema will be modified according to the needs and imported.
  - Inside the `infered_schema.py` you can explain the automatically generated validations using `Checks` and all parameters for each column.
  - Mention that this automatic schema it’s just to reduce the boilerplate and should be customized.
  - The customized schema is in `altered_schema.py` and this one will be used for validations.
    - The comments show exactly what was changed from the `infered_schema.py` to the `altered_schema.py`
    - There are some non-sense `checks` that were customized and other `nullable` parameters.
    - This step could be called a data quality and/or business rule specification.
- After explaining the automatic schema inference, you can just show how to use it with the `@pa.check_output(schema, *lazy*=True)` in `pa_validation_decorator.py`.
- Considerations:
  - All scripts that validate datasets use `lazy=True` and a `try-except` block catching specific `pa.errors.SchemaErrors` in order to show a report containing the failure validations and cases

## Conclusion

- pandas is a great data analysis tool and pandera is specific for data validation.
- pandas have low support for strongly type hints
- Pandas do not validate but infer data types.
- Pandera can be used to extend type hints for pandas, but it is much more powerful than that.
- It’s possible to check (or not) if the schema in type hints is compliant with the dataframe.
