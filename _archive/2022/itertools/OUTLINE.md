## What is an Iterator?

- An iterator is an object that can be iterated upon, meaning that you can traverse through all the values.
- What this means in Python is that an iterator is an object which implements the iterator protocol, which consist of the methods **iter**() and **next**().
- Iterators are everywhere in Python. They are elegantly implemented within for loops, comprehensions, generators etc. but are hidden in plain sight.

## Iterator vs Iterable

- You might have heard both terms being used → they’re not the same thing!
- An iterable is an object that you can get an iterator from using the iter() method.
- An iterator is an iterable that also has a next dunder method to get the next element.
- Lists, tuples, dictionaries, sets, even strings are all iterables. By calling _iter_, you can get an iterator from them. By the way, I find how iterators and iterables are organized a bit strange. It means that each iterator can return another iterator, and so on… I’m not sure I understand the function of this, perhaps this offers a mechanism to ‘restart’ an iterator (REVIEWERS: do you have any idea?)
- Show iterator examples (`iterator_basics.py`), using `next`, using a for-loop and show the equivalent while-loop.
- The built-in function iter() can be called with two arguments where the first argument must be a callable object (function) and second is the sentinel. The iterator calls this function until the returned value is equal to the sentinel.
- Iterables provide a nice way of abstracting the data structure from the code that traverses it. See for example `iterator_abstraction.py`. You can replace the `line_items` list by a tuple or a set (provided you add a hash dunder method), and the `print_totals` function works because it only expects an iterable.

## Build your own iterators

- Building an iterator from scratch is easy in Python. We just have to implement the **iter**() and the **next**() methods.
- The **iter**() method returns the iterator object itself. If required, some initialization can be performed.
- The **next**() method must return the next item in the sequence. On reaching the end, and in subsequent calls, it must raise StopIteration.
- Iterators can be finite or infinite
- Show `custom_iterator.py`

## Itertools

- Itertools is a module that provides functions that work on iterators and produce more complex iterators. Together this forms an iterator algebra.
- For example, let’s say you have a list of prices and quantities and you want to create another list containing the subtotals. You could do this naively with a for-loop and compute it yourself, or, you could use the `starmap` function, provide it with a multiplication function and a an iterable of tuples as the second parameter.
- Itertools has quite few useful functions like that and you can combine them in various ways to create complex iterator behavior. It’s also pretty fast and memory-efficient.
- Show examples (see `itertools_examples.py`)

## Final thoughts

- So, what are some not-so-common ways in which you use iterators or itertools in your Python? Let me know in the comments. I’ll collect them and then perhaps I’ll do an out-of-the-box usage of itertools follow-up video in the future.
