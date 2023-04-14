## About this video

The code smells video from a couple of weeks ago did really well, so I've decided to do another one!

## Video outline

A couple of weeks ago I did a video about code smells. If you haven't watched that yet, I posted a link to it in the comments. I really enjoyed recording that video and you seemed to like it too, so I'm doing another one. I'll also give you a tip on what you can do to avoid code smells in general.

If you're new here and you want to become a better software developer, gain a deeper understanding of programming in general, start now by subscribing and hitting the bell, so you don't miss anything.

### Explain the example

## What are code smells?

Recap: a code smell is not a bug, it's more of a hint that something's wrong in your code. It can be a minor thing that's easy to fix. Or, it can point to a bigger problem in your design. Today, I'll cover 7 more code smells. Not all of them are Python-specific by the way. But regardless, they're still pretty smelly!

### Code smell #1: Large number of arguments

(see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-107](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-107))

The `add_vehicle_model_info` method has too many parameters. Two reasons:

1. It's copying over all of the parameters from `VehicleModelInfo`, so we can better use `VehicleModelInfo` directly instead. This is also related to another smell called the 'feature envy smell' where an object or method needs to know too many implementation details of another object, suggesting they should be merged, or split differently.
2. `VehicleModelInfo` doesn't declare any defaults, which can reduce the number of parameters needed.

Solution: directly add `VehicleModelInfo` object instead of passing all the attributes as arguments, and define a few sensible default values in `VehicleModelInfo`. Rename the method to `add` since it's clear we're adding `VehicleModelInfo` object.

Overall: avoid methods with more than 3 or 4 arguments.

### Code smell #2: Too deep nesting

( see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-1066](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-1066))

Too deep nesting is generally a sign of code that has low cohesion (too many responsibilities). `register_vehicle` has too deep nesting. It has both the job of finding vehicle information, as well as generating a license and an id. A second issue is that the nesting can be further simplified by using Boolean logic.

Solution: create a separate `find_model_info` method and call that, and combine the if-statements into a single one with the `or` operation. Bonus: show the difference between handling the special case (vehicle info not found) first vs after and the effect on code nesting.

### Code smell #3: Use the right datastructure

If you need to iterate over all `VehicleModelInfo` objects just to find one with a specific brand+model, you probably want to use a dictionary instead, and key it on (str, str) tuples.

Solution: convert the datastructure to a dict with (str, str) tuples as keys.

Note:

- This also significantly simplifies the `find_model_info` function!

### Code smell #4: Using nested conditional expressions

(see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-3358](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-3358))

When you use nested conditional expressions the code becomes really hard to read. An example is the `online_status` method: it's hard to understand what the result is in which situation.

Solution: split the conditional expression into two. Actually, I must say I almost never use these myself. Often I find a regular if-statement cleaner, even though it's not as short. I'd say a conditional expression is useful if the variable names and results are short so it fits comfortably in a single line.

Notes:

- The `online_status` method doesn't do that much in this particular example, it's mainly there to demonstrate the smell.

### Code smell #5: Using wildcard imports

(see [https://rules.sonarsource.com/python/type/Code Smell/RSPEC-2208](https://rules.sonarsource.com/python/type/Code%20Smell/RSPEC-2208))

Both random and string use a wildcard import. Don't do this because it clutters up the namespace and may lead to you accidentally redefining functions or variables that you shouldn't. Also, it's unclear whether things come from random or from the string library, which is confusing. For instance, does the `choices` function come from random or string? And how about the `digits` variable?

Solution: replace the wildcard import by importing the module directly (i.e. `import string`).

Notes [not in screencast but regular!]:

- Rule of thumb: always just import the module, unless there is a good reason not to (for instance in the case of dataclasses or datetime, it's completely clear what it is and they can be used in different places in the module)
- If the module name is too long, you can alias it to a shorter name. Example: `import pandas as pd`.

### Code smell #6: Asymmetrical code

(see [https://wiki.c2.com/?AsymmetricalCode](https://wiki.c2.com/?AsymmetricalCode))

Both `Vehicle` and `VehicleModelInfo` have a method that returns a string representation of the object. But they have different names. Asymmetrical code is when you have similar code in different places that is named or handled differently.

Solution: replace both by the built-in `__str__` function.

Notes [not in screencast but regular!]:

- `__str__` vs `__repr__`. When to use which one? Use the former for more human-readable strings, and the latter to produce Python code that can be evaluated to produce the same object. I generally keep the distinction between `__str__` for users, and `__repr__` for developers.

### Code smell #7: Methods that don't need self

If a method doesn't use self, it should be a static method. This is the case for the methods that generate an id and that generate a license.

Solution: simple, remove self. And as a bonus, let's improve the clarity of the license generating method by splitting out the string parts.

By the way, Python has class methods and static methods. These are not the same thing! Both are bound to a class instead of to an object. However, a class method has access to the class state. So it can for example change the value of a class variable which is then applicable to all instances. A static method can't do that. It's simply part of a class because it makes sense.

### Code smell #8 (BONUS): Not using a main function in a module

If you don't use a main function, this means that any variables you declare under the `if __name__ == "__main__":` part are in the global scope of the module, which can lead to unexpected bugs, shadowing variables that you also use somewhere else, etc.

Solution: put everything into a separate main function and directly under the `if...` part.

### Final thoughts

It's good to know about these smells, but if you want to avoid code smells, there are tools to help you. I use VS-Code as my editor, and I'm using a combination of Pylint, Pylance and Black, which solves already a lot of issues for me. Pylint is mainly useful for style issues. Pylance adds lots of features to VSCode such as better syntax highlighting, type checking and automatic imports. Finally, Black is a really nice autoformatter. I just set it to format my code whenever I save the file. It's opinionated so I don't have to think about it.

Another thing you can do is make sure to understand your problem, before you start solving it. I wrote a free guide to help you with this. You can get it at arjancodes.com/designguide. It describes in 7 steps what I generally do when designing new software. I've kept it pretty short and to the point, so you can go through it quickly and apply it immediately.

I hope you enjoyed this video. Now let's go and cleanse ourselves. Or perhaps you like dirty. I think it's time to end this. Thanks for watching, take care and see you next time!
