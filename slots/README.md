# Introduction

# How do classes work in Python?

Classes store the attribute values in `__dict__`. In Python, attributes are not declared in advance, but they're created dynamically. You normally do this in the init method though you can do it in any method, and at any time. Because of that, classes maintain a dictionary of what the current attributes are.

(show example of simple class and print the `__dict__` value)

However, for small classes with known attributes it might be a bottleneck. The dict wastes a lot of RAM. Python can’t just allocate a static amount of memory at object creation to store all the attributes. Therefore it uses a lot of RAM if you create a lot of objects. Dictionaries in Python are implemented as a hashmap. Even though this means that lookup is pretty fast, with a worst case scenario of O(1), there's still hashing involved, and the structure in memory might not be the most efficient, in particular for larger dictionaries.

So what can you do to make your classes more performant? I'll show you that you can add a single line of code to your class to get a performance improvement of about 20%. Before I dive into this, we need to learn about descriptors.

# What is a descriptor?

In general, a descriptor is an attribute value that has one of the methods in the descriptor protocol. Those methods are **get**(), **set**(), and **delete**(). If any of those methods are defined for an attribute, it is said to be a descriptor.

Descriptors in Python are implemented in C and are really efficient.

# Slots

If you don't need dynamic attributes (which honestly, most classes don't need in my opinion), you can use something called slots. With slots, you define statically what the attribute names are of a class. Python then automatically generates descriptors for each attribute, which are highly efficient.

(show test with descriptors)

# Slots and dataclasses

It is a bit cumbersome to add the slots definition to a regular class. If you're using a dataclass, you can set the slots flag to True in the decorator and the dataclass will use slots, leading to the same performance boost.

# Limitations of slots

- You can't use them with mixins and multiple inheritance in general (but mixins are bad anyway, so good riddance). If you use them as part of your own code, you can probably work around this. If you provide the class in a package that others are using, moving to slots will improve performance, but it also potentially breaks the code of anyone using your package.
- You can still add attributes dynamically by added dunder dict to the slots list, but it is cumbersome. But honestly, I think it's a good thing to fix the attribute names of your classes, since it forces you to think carefully about the structure of your objects.
