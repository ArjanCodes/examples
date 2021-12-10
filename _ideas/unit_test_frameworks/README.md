# Differences between pytest and unit test

1. Pytest is a third party library you need to install. Unittest is included in Python
2. Pytest uses simple functions that can be organized into classes if you want to. Unittest groups tests into classes, leading to a bit more boilerplate code.
3. Pytest relies more on the builtin assert, unittest has assert methods. Advantage of builtin assert is that it's often shorter. The disadvantage is that the actual tests look different (e.g. raises uses a context manager)
4. Pytest has error color highlighting and shows the actual code where things went wrong. Unittest only displays the line number and a traceback.
5. Pytest has way more advanced options. I'll talk about a few of them in this video.
6. Pytest at the moment doesn't integrate all that well with type hints.

# Fixtures

If several tests rely on the same underlying test data, you can create a so-called fixture that is then used in one or more tests. In unittest, you do this by creating a setUp method in the testing class that then creates an object stored as a member in a class. Pytest has a fixture decorator, and then if you add the name of the fixture as an argument to your testing function, pytest automatically passes an instance of the fixture to the function. You can control how often a new instance is created by defining the scope of a fixture (function, module, package, ...). Most of the times, your testing functions will use fresh instances, so the scope is "function". But in some cases it's useful to have module-scoped fixtures, for example if you create a fixture for http requests that always return code 200, you don't to create new instances all the time.

# Fixture variations and property-based testing (screencast)

Fixtures are great for extracting data or objects that you use across multiple tests. They aren’t always as good for tests that require slight variations in the data. Littering your test suite with fixtures is no better than littering it with plain data or objects. It might even be worse because of the added layer of indirection. If your goal with this is property-based testing, you can use the parameterize decorator to do this (see example code).

# Running the tests

Unittest: python -m unittest discover
Pytest: pytest
