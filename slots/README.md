# Introduction

# How do classes work in Python?

Classes store the attribute values in `__dict__`. This is really helpful as it allows setting arbitrary new attributes at runtime.

(show example of simple class and print the `__dict__` value)

However, for small classes with known attributes it might be a bottleneck. The dict wastes a lot of RAM. Python can’t just allocate a static amount of memory at object creation to store all the attributes. Therefore it uses a lot of RAM if you create a lot of objects. Also, a dictionary in Python is implemented as a hashmap. This means that for attribute lookup, the worst case scenario is O(n).

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

- Don't use them with mixins (but mixins are bad anyway, so good riddance).
- You can't dynamically add attributes anymore. But honestly, I think that's a good thing as well, since it forces you to think carefully about the structure of your objects.
