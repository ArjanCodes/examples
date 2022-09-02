# Introduction

Since Google is a highly data-driven company and also does "a couple of things" with machine learning, I'm quite certain that a lot of people at Google use Python. But how do they do that? Are they writing Python code differently than us mere mortals?

One of my viewers recently pointed me to a document containing Google's guidelines for writing Python code for people working on Google code.

# 1: Main

In Python, pydoc as well as unit tests require modules to be importable. If a file is meant to be used as an executable, its main functionality should be in a main() function, and your code should always check if **name** == '**main**' before executing your main program, so that it is not executed when the module is imported.

Another reason to use a main function is that you don't pollute the module namespace with any variables if you can declare them locally in main().

# 2: Use imports only for packages and modules

# 3: List comprehensions

Okay to use for simple cases. Each portion must fit on one line: mapping expression, for clause, filter expression. Multiple for clauses or filter expressions are not permitted. Use loops instead when things get more complicated.

# 4: Default argument values

Often you have a function that uses lots of default values, but on rare occasions you want to override the defaults. Default argument values provide an easy way to do this, without having to define lots of functions for the rare exceptions. As Python does not support overloaded methods/functions, default arguments are an easy way of “faking” the overloading behavior.

Default arguments are evaluated once at module load time. This may cause problems if the argument is a mutable object such as a list or a dictionary. If the function modifies the object (e.g., by appending an item to a list), the default value is modified. So, do not use mutable objects as default values in the function or method definition.

# 5: Properties

Properties may be used to control getting or setting attributes that require trivial computations or logic. Property implementations must match the general expectations of regular attribute access: that they are cheap, straightforward, and unsurprising.

# 6: Getters and Setters

Getter and setter functions (also called accessors and mutators) should be used when they provide a meaningful role or behavior for getting or setting a variable’s value.

In particular, they should be used when getting or setting the variable is complex or the cost is significant, either currently or in a reasonable future.

If, for example, a pair of getters/setters simply read and write an internal attribute, the internal attribute should be made public instead. By comparison, if setting a variable means some state is invalidated or rebuilt, it should be a setter function. The function invocation hints that a potentially non-trivial operation is occurring. Alternatively, properties may be an option when simple logic is needed, or refactoring to no longer need getters and setters.

Getters and setters should follow the Naming guidelines, such as get_foo() and set_foo().

# 7: Lexical scoping

A nested Python function can refer to variables defined in enclosing functions, but cannot assign to them. Variable bindings are resolved using lexical scoping, that is, based on the static program text. Any assignment to a name in a block will cause Python to treat all references to that name as a local variable, even if the use precedes the assignment. If a global declaration occurs, the name is treated as a global variable.

# 8: Exception handling tips

- Make use of built-in exception classes when it makes sense. For example, raise a ValueError to indicate a programming mistake like a violated precondition (such as if you were passed a negative number but required a positive one).
- Do not use assert statements for validating argument values of a public API. assert is used to ensure internal correctness, not to enforce correct usage nor to indicate that some unexpected event occurred. If an exception is desired in the latter cases, use a raise statement.
- Libraries or packages may define their own exceptions. When doing so they must inherit from an existing exception class. Exception names should end in Error and should not introduce repetition (foo.FooError).
- Never use catch-all except: statements, or catch Exception or StandardError, unless you are
  - re-raising the exception, or
  - creating an isolation point in the program where exceptions are not propagated but are recorded and suppressed instead, such as protecting a thread from crashing by guarding its outermost block.

Python is very tolerant in this regard and except: will really catch everything including misspelled names, sys.exit() calls, Ctrl+C interrupts, unittest failures and all kinds of other exceptions that you simply don’t want to catch.

- Minimize the amount of code in a try/except block. The larger the body of the try, the more likely that an exception will be raised by a line of code that you didn’t expect to raise an exception. In those cases, the try/except block hides a real error.

- Use the finally clause to execute code whether or not an exception is raised in the try block. This is often useful for cleanup, i.e., closing a file.

# Resources

- https://google.github.io/styleguide/pyguide.html
