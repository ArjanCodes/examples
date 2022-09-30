# 7 things you need to know about Python 3.11

The new Python 3.11 is here. There are quite a few changes, and not all of them are immediately obvious when you look through the release notes. I'm going to cover 7 things today that I think you should know about Python 3.11, because they're going to make your life a lot easier.

## 1. Tomllib

The first thing that's going to be handy is that tomllib is now part of the Python standard library. This allows you to read files written in the TOML format. The acronym stands for 'Tom's Obvious Minimal Language'. The format is specifically targeted to using it with configuration files. And especially for configuration settings, I do think it's more readable than JSON or YAML.

https://peps.python.org/pep-0680/

See `toml_example.py`.

## 2. Exception notes

Another useful new feature is that you can now add notes to Exceptions by using the `add_note` method that's been added to `BaseException`. The idea is not to now start using exceptions for all your note-taking needs. There are better apps for that. But, you can now add some extra information to an exception when you catch it. This can be helpful if you want to provide extra context about why the exception occurs before reraising it.

Interesting note: this was contributed by Zac Hatfield-Dodds who's the developer behind the Hypothesis testing package. I did a video about that package a while ago, check it out here if you'd like to watch it.

A testing library like Hypothesis creates all kinds of extra data like failing examples in a unit test, and now you can use `add_note` to directly add this type of information to an exception object.

https://peps.python.org/pep-0678/

See `exception_notes.py` example.

## 3. More precise error location in traceback

When an error occurs, Python normally prints a traceback message, so you can try to figure out what happened. Until now, Python simply printed the line on which the error occurred, but didn't give anymore specific information about where in the line of code the issue was. That's changing in version 3.11. Tracebacks now give a precise location of the expression that caused the error. This is in particular helpful if you're dealing with more complex objects or multiple function calls in a single line. It's a relatively small thing, but it's going to save you time locating errors and fixing them.

(Show screenshot of traceback info from the release notes)

## 4. Arbitrary literal string type

Before Python 3.11, there was no way to to specify, using type annotations, that a function parameter can be of any literal string type. You can pass a string as a parameter, which is of type `str`, but a string can be constructed in lots of different ways and you might not want that. Alternatively you can pass a specific literal string, like `Literal["ArjanCodes"]` but then it will only accept that specific literal string. PEP675 introduces the `LiteralString` type which accepts any literal string.

Why is this useful? In particular this is helpful when you're invoking SQL or shell commands. These kinds of systems often prefer to be invoked using literal strings in order to avoid security vulnerabilities. The PEP definition itself contains an example of this. Here, a SQL query is constructed using an f-string, which allows for an injection attack. Though SQL APIs offer parameterized queries to avoid this issue, there's no way to enfore it using type annotations. Since the new version of Python, you can use the `LiteralString` type to do this.

https://peps.python.org/pep-0675/

(show screenshot of literal string type example from the PEP)

## 5. Self type

Another nice new feature of the new Python version is that there's now a Self type (with capital letter). In the past, if a method in a class returned a value of the type of that class, you had to either write the type between quotes, or use the kind of hacky feeling "from **future** import annotations" line. And by the way, merging the **future** module directly into the Python language, has been postponed indefinitely in this release. So, dunder future is no longer the future.

Being able to use Self instead of the class name directly is nice. If you change the class name, you don't have to change the method return value.

When is this useful? I sometimes like to use static methods in a class to create an object. It's a way to offer different options to create an object. I have an example here.

See `self_type.py` example, and show the difference between returning "Piece", Piece with future type annotations and the Self type.

## 6. String enums

There's a new StrEnum type. If you use this in combination with auto, it's going to automatically create string names from the enum values.

See `str_enum.py` example.

## 7. Faster Python

Finally, one more thing that's going to significantly impact you is that Python is getting a lot faster with this release. You'll see performance improvements between 10-60% depending on what features you're using.

The reason is that CPython 3.11, the reference Python implementation used by most people, is on average 25% faster than CPython 3.10. There's both a faster startup of the Python interpreter as well as a faster runtime execution. Interpreter startup is about 10-15% faster. For running Python code, there's been a performance improvement to lots of basic operations like binary operations, attribute assignment, some function calls and subscripting.

Let's take a look at a few examples.

https://docs.python.org/3.11/whatsnew/3.11.html#faster-cpython

Show the Dijkstra program (`dijkstra.py`) as well as the class test program (`classtest.py`).
