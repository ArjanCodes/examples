## Intro

Person A: Type hints are great, I use them all over my code. I love them!

Person B: I hate type hints. They're useless in Python, it's extra work to write them, most libraries don't have them, so why bother?

Person B has some good points. And there are more criticisms on using type hints, even by Guido himself, which I'll cover in a minute. I'm going to talk about the issues with type hints, and then I'll share the reasons why in spite of those issues, I still use them all over the place in my code examples. After watching this video, I hope you'll have a better understanding of type hints, and that this will help you make a decision about whether you should use type hints, or not. The choice is yours.

Before we dive in, I have something for you. It's a free guide to help you with designing a new piece of software in 7 steps. It's available at arjancodes.com/designguide. It's a PDF file containing the steps that I take myself, and hopefully this helps you avoid some of the mistakes I made in the past. If you enter your email address on the page, I'll send the guide to your inbox. Arjancodes.com/designguide, the link is also in the description of this video.

## What are type hints? (screencast)

- Show an example: the `luhn_checksum` function with arguments and a return value
- Add type hints, also to the `digits_of` function

By the way, if you're enjoying this video so far, give it a like. It helps others find this content on YouTube as well.

## Criticisms of type hints

Some common criticisms of type hints that I hear:

- I don't see the benefit of using type hints in a duck-typed language. They've never helped me out.
- BDFL Guido was quite clear, they never intend for types to be enforced in python: "Python will remain a dynamically typed language, and the authors have no desire to ever make type hints mandatory, even by convention." See also: [https://peps.python.org/pep-0484/](https://peps.python.org/pep-0484/).
- Type hints artificially limit your code: especially more generic functions might work with a wider set of types than what you can specify (think of sorting algorithms, etc.)
- Not all libraries in Python have type hints, so why bother?
- It's extra work to add type hints tp a Python program, but the interpreter ignores them, so what's the purpose?
- If you're testing your code already, why not simply add the tests for type correctness as unit tests?

Yet, I use types extensively in the code that I write. Why is this?

## Reasons to use type hints

### Types help me avoid write documentation.

If you look at a Python function header that doesn't use type hints for its arguments, you need documentation in order to understand what you should provide to that function. I really hate writing documentation:

- it's very easy to become outdated, and you need to manually check that it's still correct
- if code has too much documentation, it actually becomes harder to read

If there is no documentation at all, you might need to read the body of the function to understand what a function is doing, so of course, documentation can be useful in some cases.

But I'm all in favor of doing things to keep documentation simpler if possible. Types are a standardized way of specifying what an argument should look like and what kind of thing a function (or method) returns. Because it's a natral part of the function/method header, I find it's much easier and faster to read than putting those things in the function/method's documentation.

### Types are helpful while writing code in your IDE

- The IDE can then detect sooner if you're passing the wrong kind of data structure
- The IDE provides autocomplete for data structures that it knows

In the PEP I mentioned in the beginning of the video, the authors also write this: "This PEP aims to provide a standard syntax for type annotations, opening up Python code to easier static analysis and refactoring, potential runtime type checking, and (perhaps, in some contexts) code generation utilizing type information.". The first part of this in particular makes it easier for IDEs to use type information.

#### Luhn checksum with/without docs and type hints

- In the untyped version, it's not clear what the type of `number` is. You might expect it's an int, but it's actually a string. If you use an int, you get a cryptic error message.
- In order to figure out the type, you need to dive into the function body.
- Adding documentation helps, but who reads documentation? And you can still call the function with an int, and the IDE won't complain
- If you want the IDE to complain so you avoid the error altogether, use type hints!

### Types make coupling more explicit

By using and sharing type definitions between modules, it's easier to see which modules are coupled to certain data structure. This is especially helpful if in the future you decide to change that data structure, because then you want to know which modules are going to be affected.

### Using type hints forces you to be explicit about the data structures you use

- Having a clear idea of what the data looks like helps a lot when you design a piece of software. With types, you define this explicitly in the language.
- Types also discourage behavior that potentially leads to messy code, such as:
  - changing data structures on the fly (like dynamically adding attributes to an object), or
  - creating data structures that are too large, leading to loss of cohesion

### Using type hints simplifies your code

Often, untyped Python code has if-statements in the function body to check that the argument you get is actually what you expect it to be. Types help reduce this kind of code. Though to some extent, you might still need it, in particular if you're relying on data read from a file where you have no control over the structure. A better solution in this case though is to rely on a validation tool, like Pydantic. You can then provide feedback to the user right after they try to import their crooked, badly formatted data.

## Type hints vs using unit tests

Instead of using type hints, you can also write unit tests to check that the data that is passed to a function or method does indeed follow what you expect it to be. In a language where type definitions aren't obligatory, like Python, this can make sense. But, you'll lose out on all the advantages that I mentioned just now. And in addition, writing a type hint is faster than writing a bunch of unit tests. Especially for more complex data structures, this might become a lot of work.

## Final thoughts

Overall, my goal is to write my code as fast as possible. I want to get things done. Clarity of mind helps me do that, and I find that types have helped me a lot in providing that clarity. It makes me think about the structure of my data, it makes it easier for me to figure what that function is supposed to do that I wrote a couple of months ago, and I can keep my unit tests focused on testing the actual behavior of my functions and methods instead of cluttering up the unit tests with type checks.
