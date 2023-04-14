# Introduction

What do think of my new recording setup? If this is the first video you're watching of me, well, my previous videos don't look as cool as this one. So, you came in at the right time.

If you're using classes in Python, did you know you can increase your code's performance with about 20%, by adding a single line of code to your class? I'm going to show you how you do this, also if you're using dataclasses. And then I'll do some performance comparisons as well.

Before I dive in, I have something for you. It's a free guide that describes the 7 steps I take whenever I design a new piece of software. You can get it at arjancodes.com/designguide. If you enter your email address there, you'll get it in your inbox. It's a PDF file, that's to the point, and it contains practical tips to help you make better design decisions. So, arjancodes.com/designguide. The link is also in the description of this video.

# How do classes work in Python? (couch)

Classes store the attribute values in `__dict__`. The resaon is that in Python, attributes are not declared in advance, but they're created dynamically. You normally do this in the init dunder method though you can actually do it in any method, and at any time. Because of that, classes in Python maintain a dictionary of what the current attributes are.

(show example of simple class and print the `__dict__` value)

However, for small classes with known attributes this might turn into a bottleneck. There's more information in a dictionary than just the key-value pairs, and because they're dynamic, Python can’t just allocate a static amount of memory at object creation to store all the attributes. So, this leads to a lot of RAM usage if you create many objects. There's also another performance penalty you pay with a dictionary. Dictionaries in Python are implemented as a hashmap. Even though this means that lookup is pretty fast, it's generally going to be O(1), there's still hashing involved, and access is going to be slower than reading from a highly optimized array in memory.

So what can we do about this? Before showing you how to make your classes way more performant, we first need to learn about descriptors because they play an important role here.

# What is a descriptor? (talking head A)

In general, a descriptor is an attribute value that has one of the methods in the descriptor protocol. Those methods are **get**(), **set**(), and **delete**(). If any of those methods are defined for an attribute, it is said to be a descriptor.

Descriptors in Python are implemented in C and are really efficient.

By the way, if you're enjoying the video so far, give it like. It helps the mighty YouTube algorithm to spread the word so others can find this content as well. And of course it strokes my huge ego, so there's that as well.

# Slots (Screencast)

If you don't need dynamic attributes (which honestly, most classes don't need in my opinion), you can use something called slots. With slots, you define statically what the attribute names are of a class. Python then automatically generates a descriptor for each attribute, which are highly efficient.

(show test with descriptors)

By the way, if you're enjoying this video so far, give it a like. It helps others find this content on YouTube as well.

# Slots and dataclasses

It is a bit cumbersome to add the slots definition to a regular class. If you're using a dataclass, you can set the slots flag to True in the decorator and the dataclass will use slots, leading to the same performance boost.

# Limitations of slots

- You can't use them with mixins and multiple inheritance in general (but mixins are bad anyway, so good riddance). If you use them as part of your own code, you can probably work around this. If you provide the class in a package that others are using, moving to slots will improve performance, but it also potentially breaks the code of anyone using your package.
- You can still add attributes dynamically by added dunder dict to the slots list, but it is cumbersome. But honestly, I think it's a good thing to fix the attribute names of your classes, since it forces you to think carefully about the structure of your objects.
