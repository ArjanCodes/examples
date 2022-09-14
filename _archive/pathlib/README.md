# Pathlib tutorial

If you're not using pathlib yet for anything related to dealing with files and folders, you're missing out. This video is a deep dive into Python's pathlib library, that been available since Python 3.6.

I'm not just going to talk about pathlib and what you can do with it, but also about how some of the magic behind the library works and how you can apply this same magic to your own code.

If you want to learn more about how to design software from scratch, I have a free guide for you. You can get it at arjan.codes/designguide. It contains the 7 steps I take when I design new software, and hopefully it helps you avoid some of the mistakes I made in the past. I've tried to keep the guide short and to the point, so you can get the information quickly and apply it immediately to what you're doing. So, arjan.codes/designguide, and the link is also in the description of this video.

## Why not simply use strings

So, you might say, why do we need a library for dealing with paths? Can't we just use strings? Well, yes, you certainly can. In fact, this was the way that most packages in Python dealt with paths before version 3.6. If you use strings to represent paths, you're going to run into a couple of very annoying issues:

1. If you want to construct paths from parts, it's a pain. If you use os.join for this, it quickly becomes code that's hard to read.
2. Depending on the platform there's a diffent way that paths are represented (posix vs windows, or forward slashes vs backward slashes). If you forget to take this into account, your code only works on one of the two platforms.
3. There's some information you want to commonly access: the parent folder, the file extension, whether something is a file or a directory, and so on. If you're using strings, you have to write the code for this yourself (and hope it doesn't contain bugs).

Now I must also admit that in past videos, I regularly didn't use pathlib. Why not, you ask? Well, in Dutch there's a nice expression for this: "voortschrijdend inzicht". In English this roughly translates to "progressive insight", but I'm not sure it covers the nuance of the Dutch version. In any case, you learn and improve along the way and that's what I'm doing as well. So, expect more appearances of pathlib in my videos in the future.

## Basic usage of pathlib

What's nice about pathlib is that it is an object-oriented way of dealing with paths. Paths are objects, and they have useful methods and operations you can perform on them. Let's take a look at a few examples.

Go through `examples.py`.

## Some background on the slash usage in pathlib

As you've seen, one of the nice things about pathlib is that there's a really cool way to construct paths using the slash operator which relies on some Python magic. Not all magic is good (ahem Pandas query), but this is pretty cool.

How does this work? It relies on a programming feature called operator overloading. The slash is the division operator, and Python allows you to define what the behavior of an operator is when used with an object of a particular type. Many other programming languages have this feature as well by the way. I fondly remember implementing operator overloading in C++ when working on a game engine used for research in the beginning of the 2000s.

Anyway, let's take a quick look at how you can do operator overloading in Python. (show example of operator overloading using a Point class - see `operator_overloading.py`).

A remark about passing an int to something that's annotated as a float type. This is possible because float is treated as a special case. PEP 484 writes this: "when an argument is annotated as having type float, an argument of type int is acceptable". This special treatment is basically a shortcut. Arguments that can be a float or an int are quite common, so in this way you don't have to write "float | int" but you can simply write float and then it also accepts integer values.

See also: https://peps.python.org/pep-0484/

## Pathlib and Pydantic

It's quite common to set paths in configuration files, think of specifying the folder where your sample data is stored, where to output log files, and so on.

You can use simple dataclasses to deal with config settings. If you want to learn more about dataclasses, check ou tthis video where I dive into dataclasses. Unfortunately, dataclasses don't have built-in support for processing and dealing with paths (in other words: paths are simply represented as strings, even if you define the dataclass instance variable as a path. (if you create a Settings instance instead of a PySettings instance in `pydantic_example.py`, it won't work correctly as the string is not transformed into a path). If you're using Pydantic, this is done automatically for you.

## Outro

I hope you enjoyed this deeper dive into pathlib. If you did, you might also like this video where I dive deeper into Python's string formatting capabilities. Give this video a like and consider subscribing to my channel if you want to learn more about software design and development. Thanks for watching, take care, and see you next time.
