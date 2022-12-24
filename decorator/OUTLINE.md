- If you’re doing purely object-oriented programming, then the common way to reuse functionality is by using inheritance.
- However, inheritance doesn't always work out well. Some aspects of a software design are orthogonal to the class hierarchy. These are sometimes called "cross-cutting concerns". They cut across the classes, making design more complex.
- The logging I mentioned in the beginning is a good example. Lots of functions or methods might have logging that you want to be consistent, but classic inheritance doesn’t offer a simple mechanism to add logging to all the methods. Other examples are security (authentication checks), benchmarking or user analysis.
- Ideally, you’d want to take an existing object or function and “add” behavior to it such as logging or benchmarking.

## Object-Oriented decorator

- Classic version
- Version that uses callable

## Functional decorator

- Show that you can simply wrap a function into another function to add functionality

## Functools wraps

- If you just wrap a function around another function, printing the name doesn’t always provide the correct result.
- Use functools.wraps to solve this!

## Should you use decorators?

- You might be tempted now to use decorators for everything. Looks cool, right?
- Watch out though: decorators may make your code harder to read because it’s not always clear how a decorator call the function that it decorates. This might lead to bugs that are hard to solve. Especially if you didn’t build the decorator yourself but you used an external package.
- Some decorators modify the signature of the function they decorate. For example, the hydra package does this: it adds an argument to the function that contains a configuration object it read from a file. This is a bad design practice as it breaks the type checker!
- I think decorators work well for lower-level things like properties, data classes, or simple wrappers for logging or benchmarking. For more high-level things, I typically don’t use decorators myself, but will opt for simpler designs using functions and composition. Especially if you’re solving a complex design problem, relying on basic features of the language wherever you can will probably lead to more readable code that’s easier to maintain in the long term.
