## Overview

- pandas is a fast, powerful, flexible and easy-to-use open-source data analysis and manipulation tool, built on top of the Python programming language.
- But you might run into problems if you’re using pandas for larger datasets.
- You might just blame Python for being slow, but probably the reason is memory consumption.
- Today I’ll show you a simple change in how you use pandas that will reduce the memory your script uses by over 90%.
- Before I dive into that, it’s important to learn a bit more about pandas data structures and types.

## About pandas

- it’s an external dependency, and it should be installed with `pip install pandas`
- There are two main data structures in pandas: `DataFrame` and `Series`
  - `DataFrame` is equivalent to a table with columns and rows
  - `Series` is one column of a `DataFrame`, and basically a pair of key-value for rows and the specific column.

## Types in pandas

- For the most part, pandas use NumPy arrays and dtypes for `Series` or individual columns of a `DataFrame`.
- NumPy provides support for `float`, `int`, `bool`, `timedelta64[ns]` and `datetime64[ns]`
- NumPy does not support timezone-aware datetime
- Pandas have made some types of extensions internally, beyond what NumPy already supports
  - `DatetimeTZDtype`: a tz-aware datetime type.
  - `CategoricalDtype`: for managing categories using efficient memory use instead of a string repetition that consumes a lot of memory
  - `PeriodDtype`: used for time-series analysis that has a frequency (daily, weekly, monthly, etc.)
  - `SparseDtype`: sparse-matrix data type. A sparse matrix is a \*\*\*\*matrix that is comprised of mostly zero values.
  - `IntervalDtype`: represents an interval of either integers/float or datetime.
  - All nullable integers like `Int64Dtype`: When working with missing data, we saw that pandas primarily use `NaN` to represent missing data. Because `NaN` is a float, which forces an array of integers with any missing values to become a floating point. In some cases, this may only matter a little. But if your integer column is, say, an identifier, casting to float can be problematic. Some integers cannot even be represented as floating-point numbers.
  - `StringDtype`: **,** represents a string. I’ve never seen this in practice at all. Any columns of the string are normally kept as an `object`, or in some cases, as `categorical` using the `CategoricalDtype`
  - `BooleanDtype`: represents boolean values.
- Each one of the types above has a string representation that can be found [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#dtypes)
- Arbitrary objects may be stored using the `object` dtype
- Pandas do a good job inferring data types, but in some cases, it assumes the wrong data types.

## Type conversion

- `DataFrame.astype()`: conversion to specified types. Example:

```python
 # Converts the entire DataFrame to float32 using the string representation
df.astype("float32")

# Converts only types of columns a and c
df.astype({"a": "bool", "c": "float64"})
```

- `pandas.to_numeric`: conversion to numeric types

```python
>>> mixed = ["1.1", 2, 3]
>>> pd.to_numeric(mixed)
array([1.1, 2. , 3. ])
```

- `pandas.to_datetime()`: conversion to standard datetime type in python

## Data type inference and conversion

- See`**general_pandas_types.py`\*\*
- The `netherlands_airports.csv` contains the first line with metadata that breaks the entire pandas typing inference. All columns are read as the `object` type.
- Types of wrong typing inferences are printed out.
- After removing that metadata row, pandas can infer more accurately the correct types. Types are printed once more to show the good work of pandas.
- The `object` types are converted to a `string` and the column `scheduled_service` which contains only ones and zeros is not `int` but `boolean` instead. It’s also converted together using `.astype()`.
- Another way of conversion using `pd.to_datetime()` is shown, but this could be included in `mapping_types_conversion` as one more pair of key-value `"last_updated": "datetime64[ns, <tz>]"`. This could be also useful to define a time zone, but it’s optional.
- Last, after all, conversions, the types are printed out to show that all transformations were done successfully.
- ********\*\*\*\*********Comments:********\*\*\*\*********
  1. Although pandas did a great job after the metadata row removal, it still leads to misunderstandings types, like `last_updated` should be `datetime` and `scheduled_service` being a `boolean`.
  2. All those transformations that pandas cannot handle should be made manually.

## Optimizing memory using categorical types

- See **`categorical_type.py`**
- This script shows the huge memory reduction when using the `category` type in pandas instead of storing string data as an `object`.
- It reads a customer dataset from an e-commerce company in Brazil called Olist. It’s available in Kaggle at this [link](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) licence.
- The types before and after the transformations are printed, to show that the transformation was done successfully.
- Also, memory usage is measured before and after using the `.memory_usage(deep=True)`. the argument `deep=True` is essential here, as it reveals the real memory consumption of `object` types, as described in the method’s documentation [here](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.memory_usage.html#pandas-dataframe-memory-usage).
- There is a transformation to `category` type in three columns:
  - `customer_zip_code_prefix` that is initially stored as `int64` type.
  - `customer_city` and `customer_state` are strings stored as an `object` type.
- The percentage difference is then calculated and printed to compare the memory reduction.
- **Comments:**
  1. There is a huge shrinkage, more than 90%, in memory of memory consumption when we convert the `object` columns to `category`.
  2. This happens because the **number of categories** is much less than the number of records in the dataset, confirmed by [this section](https://pandas.pydata.org/docs/user_guide/categorical.html#memory-usage) of panda's official documentation.
  3. However, the conversion of the `int64` column to `category` type increases memory usage by 6,5%
  4. `category` type is not a NumPy array and may have some different ways when dealing with it
  5. The dataset contains only 99.441 records. The absolute difference value of memory consumption would make an even more impressive improvement if we were talking about millions of rows.

```python
>>> import datetime
>>> mixed_date_types = ["2016-07-09", datetime.datetime(2016, 3, 2)]
>>> pd.to_datetime(mixed_date_types)
DatetimeIndex(['2016-07-09', '2016-03-02'], dtype='datetime64[ns]', freq=None)
```

## Conclusion

- pandas is a great data analysis tools
- It expands NumPy and python built-in types
- Strings in pandas are mostly stored as general `objects` in practice, but it’s not recommended by the official documentation.
- If the number of records is much higher than the number of categories stored as `string` or `object`, it should be converted to `categorical` instead to optimize memory consumption.
- Pandas have several methods to infer and convert types, and within the come the parameters of the error to deal with wrong conventions.
