## Introduction

- You have at least 5 videos talking about dataclasses.
- dataclasses were added in Python 3.7 through PEP 557
- When you want to extend the class features, either you have to write a lot of code or you simply can’t do it. Examples:
  - Validate if the `price` attribute of a `Product` instance is a positive float.
    - In this case, you have to write the full validation explicitly. There are these and more of those powerful validations in `pydantic` available for direct use.
    - Another example is any percentage value that must be between 0 and 1.
  - If you want to convert an attribute to `int` in the class definition, you must write it explicitly, otherwise, the conversion won’t exist. The `attrs` has those converters and many others just ready to be used with much less code (check [here](https://www.attrs.org/en/stable/init.html?highlight=converters#converters))
- To solve those problems, it’s recommended to use either `pydantic`, a complex validation library, or `attrs`, which has much more powerful features that are not present in the standard library

## Overview

- Explain the example
  - It’s a simple e-commerce application with `Order` and `Product` classes.
  - Products have a name, category, unit price, shipping weight and a fee tax percentage.
  - Orders have a status field, a creation date and a products list associated with it.
  - It’s possible to add a product to an order
  - The sub-total gross value, tax value and final price of an order can be calculated based on the products within it.
- When we compare classes like `Product`, which should be equal when the name and category are the same, dataclass offers an option that is not the best way to do it, by defining the attribute with the `field(compare=True)`. This argument `compare` only accepts a boolean value, meaning only if the attribute is considered or not in comparison and nothing more.
- In `attrs`, the comparison feature is much more powerful. You can customize your comparison in order to use a `function` while comparing attributes in classes. An example would be `field**(**eq**=**str**.**lower**)`\*\* saying that two class instances, after applying lower to the attribute, will be considered in the comparison.
- `pydantic` uses inheritance instead and is also a complex validation library, not just a reducer for the boilerplate class generation. It also has validations for fields.

### Attribute validations

- `pydantic` has some specific types that come together with field validations. This ensures a type hint associated with an implicit validation. Examples:
  - We can set the type of customer e-mail using `email: EmailStr` which will apply some non-transparent rules to verify if the attribute is a valid e-mail.
  - Other examples are:
    - `file_path: FilePath`: like `Path`, but the path must exist and be a file.
    - `some_neg_float: NegativeFloat`: allows a float which is negative; uses standard `float` parsing then checks the value is less than 0.
    - `number: PaymentCardNumber` to parse valid card numbers with the following verifications
      - `str` of only digits, [luhn](https://en.wikipedia.org/wiki/Luhn_algorithm) valid and the correct length based on the BIN, if Amex, Mastercard or Visa, and between 12 and 19 digits for all other brands
    - `percentage: confloat(*ge*=0, *le*=1)` where you can constrain a `float` value to be in specific intervals, like percentage values.
  - The full list of type hints combined with validations can be found [here](https://docs.pydantic.dev/usage/types/) at `pydantic` official documentation.
- `attrs` has two different kinds of validation
  - using the attribute’s `validator` method as a decorator. The decorated method should have a specific signature that can be found [here](https://www.attrs.org/en/stable/init.html#decorator). Example:
  ```python
  @define
  class Customer:
      commission: float = field()
      @commission.validator
      def _check_percentage(self, attribute, value):
          if not 0 <= value < 1:
              raise ValueError(
  							"commission must be a percentage value between 0 (inclusive) and 1 (exclusive)"
  						)
  ```
  - `field` function approach
    - there is a parameter in the `field` function that can receive a validator from `attrs.validators` module or any callable with the same specification as the decorated method

## dataclasses

- **pros**
  - Standard python library → no external dependencies.
  - Since dataclasses are part of the standard library, some tools may have better support for them than for `attrs`.
- **\*\*\*\***cons**\*\*\*\***
  - Features depend on the Python version. Examples:
    - `__slots__` and `__weakref_slot__` parameters were only added in versions 3.10 and 3.11, respectively.
  - dataclasses is “just a part of” `attrs` since the third-party package has much more features.

## attrs

- **\*\*\*\***pros**\*\*\*\***
  - Supports typing, but you are not forced to use it.
  - It’s possible to customize comparisons between objects using functions that are applied to attributes. That’s not possible with dataclasses.
  - [Trusted by NASA](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/personalizing-your-profile#list-of-qualifying-repositories-for-mars-2020-helicopter-contributor-achievement) for Mars missions since 2020. (Would it be a **\*\***pro**\*\*** or just a curiosity?)
- **cons**
  - External dependency → should be installed through `pip install attrs`
  - It had incomprehensible \***\*names for the decorator in previous versions (`@attr.s` referring to attribute**s** and `@attr.ib` for a single attr**ib\**ute). It's been resolved though [in this issue](https://github.com/python-attrs/attrs/issues/408) and since version 21.3.0 there’s a new and simpler decorator called `@define`. The package names also changed from `attr` to `attrs` and thus this release is also called “The modern *attrs\*”.
  - Allows escaping from standardizations by not forcing the use of typing

## pydantic

- **pros**
  - Has an option for validation through the decorator `@validator` for fields and `@root_validator` for the entire class
  - The `Model` object that is used to create classes has a lot of already implemented helper functions ready to be used, like `.json()`, `.dict()`, `schema()`, `parse_file()`, etc. The full list of those helpers’ functions can be found [here](https://pydantic-docs.helpmanual.io/usage/models/#model-properties).
  - The behaviour control of classes in `pydantic` is defined in another class `Config`.
  - Enforces type hints at runtime.
  - Provides user-friendly errors when data is invalid.
- **cons**
  - External dependency → should be installed through `pip install pydantic`
  - Since it’s using inheritance to build classes, it does not follow the “favour composition over inheritance” design principle.
  - The validations are not clearly explained. Do the validations of type hints occurs in `__init__`? If we set the attribute, will the validation rerun?
  - Because it’s using inheritance, the classes shouldn’t have the same field name as the `BaseModel`. It would cause unwanted behaviour if the methods of the superclass are overwritten at the subclass. Can you remember all of them to avoid this?
  - Doesn't support positional arguments
  - The `__str__` generated does not contain the class name

## Final considerations

- dataclasses are from the standard library and should be preferred, but they don’t have validations like `pydantic` and have fewer features than `attrs`. The features within dataclasses also depend on the Python version. Recommended for simple class definitions
- `attrs` is an external dependency and is developed faster, therefore there are more features in `attrs` in comparison to dataclasses. The API has changed to improve names but still lacks `pydantic` validations. Recommended for more complex class definitions that do not require any extra validations.
- `pydantic` is a complex validation library, ideal if you want to validate the data in a class. It is not compliant with the design principle of composition over inheritance and enforces the use of type hints. The behaviour of classes can still be controlled through a `Config` class. Recommended for classes that enforce a large number of validations to be created.
