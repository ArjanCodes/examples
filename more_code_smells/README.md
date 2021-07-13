## About this video

The code smells video from a couple of weeks ago did really well, so I've decided to do another one!

## Video outline

- What are code smells?

  - The term code smell comes from Martin Fowler's book on refactoring.
  - A code smell is not a bug, but a hint that something's wrong in your code.
  - Code smells can be minor things, or they can point to a deeper problem/design flaw

-

### Code smell #1: Mutable default arguments

(see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-5717](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-5717))

The `add_vehicle_info` method has a `list` argument with a mutable default value. This is problematic. show by adding the following lines of code in the main function:

```python
print(add_vehicle_info("Tesla", "Model 3", True, 50000, 2021))
print(add_vehicle_info("Tesla", "Model 3", True, 50000, 2021))
```

Solution: remove the default argument from the `add_vehicle_info` function. Even better: put this function in the `VehicleRegistry` class where it belongs, and then the list argument is no longer needed.

### Code smell #2: High number of arguments

(see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-107](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-107))

The `add_vehicle_info` method has too many parameters. Two reasons:

1. It's copying over all of the parameters from `VehicleInfo`, so we can better use `VehicleInfo` directly instead. This is also related to another smell called the 'feature envy smell' where an object or method needs to know too many implementation details of another object, suggesting they should be merged, or split differently.
2. `VehicleInfo` doesn't declare any defaults, which can reduce the number of parameters needed.

Solution: directly add `VehicleInfo` object instead of via a function, and define a few sensible default values in `VehicleInfo`.

Overall: avoid methods with more than 3 or 4 arguments.

### Code smell #3: Too deep nesting

( see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-1066](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-1066))

Too deep nesting is generally a sign of code that has low cohesion (too many responsibilities). `create_vehicle` has too deep nesting. It has both the job of finding vehicle information, as well as generating a license and an id. A second issue is that the nesting can be further simplified by using Boolean logic.

Solution: create a separate `find_vehicle` method and call that, and combine the if-statements into a single one with the `and` operation. Bonus: show the difference between handling the special case (vehicle info not found) first vs after and the effect on code nesting.

### Code smell #4: Using nested conditional expressions

(see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-3358](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-3358))

When you use nested conditional expressions the code becomes really hard to read. An example is the `online_status` method: it's hard to understand what the result is in which situation.

Solution: split the conditional expression into two. Actually, I must say I almost never use these myself. Often I find a regular if-statement cleaner, even though it's not as short. I'd say a conditional expression is useful if the variable names and results are short so it fits comfortably in a single line.

### Code smell #5: Using wildcard imports

(see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-2208](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-2208))

Both random and string use a wildcard import. Don't do this because it clutters up the namespace and may lead to you accidentally redefining functions or variables that you shouldn't. Also, it's unclear whether things come from random or from the string library, which is confusing. For instance, does the `choices` function come from random or string? And how about the `digits` variable?

Solution: replace the wildcard imports by full module imports (i.e. `import string` - Code reviewer question: does this type of import has a name that I can mention for clarity?).

Notes:

- Only if it is completely clear what something is, you can use `from X import Y`.
- If the module name is too long, alias it to a shorter name. Example: `import pandas as pd`.

### Code smell #6: Asymmetrical code

(see [https://wiki.c2.com/?AsymmetricalCode](https://wiki.c2.com/?AsymmetricalCode))

Both Vehicle and VehicleInfo have a method that returns a string representation of the object. But they have different names. Asymmetrical code is when you have similar code in different places that is named or handled differently.

Solution: replace both by the built-in `__str__` function (reviewers: or is `__repr__` the better option here?)

### Code smell #7: Methods that don't need self

If a method doesn't use self, it should be a static method. This is the case for the methods that generate an id and that generate a license.

Solution: simple, remove self. And as a bonus, let's improve the clarity of the license generating method by splitting out the string parts.

By the way, Python has class methods and static methods. These are not the same thing! Both are bound to a class instead of two an object. However, a class method has access to the class state. So it can for example change the value of a class variable which is then applicable to all instances. A static method can't do that. It's simply part of a class because it makes sense.

### Final thoughts

It's good to know about these smells, but don't hesitate to use tools to help you. I use VS Code as my editor, and I'm using a combination of Pylint, Pylance and Black, which solves already a lot of issues for me. Pylint is mainly useful for style issues. Pylance adds lots of features to VSCode such as better syntax highlighting, type checking and automatic imports. Finally, Black is a really nice autoformatter. I just set it to format my code whenever I save the file. It's opinionated so I don't have to think about it.

Hope you enjoyed this example. Thanks for watching, take care and see you next time!
