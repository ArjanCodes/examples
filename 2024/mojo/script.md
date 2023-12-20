# Mojo

Ever found yourself getting annoyed how slow Python is? Let me introduce Mojo,
the new blazing fast programming languages that has all the beautiful syntax of Python, while having the type safety and
speed comparable to that of Rust.

## Introduction

Mojo is a recently developed programming language that enhances Python's syntax and incorporates both Ahead of Time and
Just In Time compilation. As a result, Mojo offers significantly improved performance compared to Python, while still
maintaining a reasonable learning curve.

However, it is important to acknowledge that Mojo is still early in a developing phase and lacks several essential features.
Many of its features are undergoing frequent modifications, and a few may not function as intended. Nonetheless, Mojo
can serve as an fun tool for experimentation and exploration.

| Feature         | Python                    | Mojo                                        |
|-----------------|---------------------------|---------------------------------------------|
| Type System     | Dynamic                   | Static + "Dynamic"                          |
| Runtime         | Interpreted               | Ahead of Time + Just In Time                |
| Type Safety     | Weak                      | Strong                                      |
| Performance     | Slower due to interpreter | Faster due to compilation                   |
| Learning Curve  | Easy                      | Medium                                      |
| Concurrency     | GIL-Locked                | Threaded Concurrency                        |
| Memory Safety   | No                        | Yes                                         |
| Garbage Collec. | Yes                       | No, uses a rust like value lifetimes system |

# What Mojo is not:

Mojo, in its current state, is not suitable for production use. There are several features that still need to be
implemented, and integrating new features can be challenging due to the current language semantics. While it can serve
as a useful coding playground, it is not yet prepared for serious professional applications. Additionally, please note
that Mojo does not currently work natively on Windows. To run Mojo, it is necessary to use the Windows Subsystem for
Linux (WSL).

>> Show hello_world.mojo

- Demonstrate the small differences in how a function is defined in Mojo vs Python, and how those you make use of type
  hints should be fairly familiar with mojo's style of declaring types.
- Explain that like most compiled languages, an entry point is required, and that this is the main function in Mojo.
- Show how we make use of var for variables, and let for immutable variables.
- Explain that all fn style functions must declare their signature.
- Explain that this is because Mojo makes use of static typing for its structs and functions.
- Note how in the function body, type "hints" are not required, but are recommended.

# Segue

If you want to see how Rust compares to Python, check out my video on Rust here.

>> show hello_world2.mojo

- Show how when using `def` style functions, we have to wrap in a try/except block, as the compiler cannot determine if
  this code will throw an error or not.
- Explain this is because mojo does not enforce the same type safety rules on 'def' style functions as it does on 'fn'
  style functions.
  This allows for more Pythonic style code, but at the cost of type safety.
  This code generally makes use of the JIT compiler, and is usually slower than the AOT compiled code.
- Explain that def style funcs with no type annotation for its return will return the dynamic 'object' type,
  This type does not follow Mojos normal semantic and can potentially lead to runtime errors, and other unexpected
  behavior.
- Explain that this is how Mojo manages type safety, and that this is how Mojo is able to be so fast.

>> show user.mojo

- Show how the struct is defined, and how it is structured similarly to a Rust struct, but bit different in the
  regard that you can define methods and functions inside the struct.
- Show the various ownership keywords, and explain that the system is similar to that of rust
- Explain that inout borrows for the duration of the function all, and that this is similar to Rusts mutable borrows.
- Explain that borrow is similar to inout, but is immutable. 
- Explain that owned take ownership of the given value.
- Explain that when mutating variables on the struct, you need to use an `inout self` parameter, this is because
  the function needs a mutable reference to self. the `__init__` function should always make sure to define self this
  way.
- Explain that the value decorator allows the value to be copied and moved around. This is similar to the `Copy` trait
  in Rust.
- Explain that Mojo does not support classes yet, but this is a planned feature.

## question
What do you think about Mojo so far, are there any features you are excited about?
Let me know in the comments below.

- Explain that DynamicVectors a similar to python lists, but can only contain a single type. They will resize themselves
  as their contents grows.
- Show that like Rust, Mojo has traits.
- Explain for those who have not seen the Rust video that traits are a type of interface.
- Explain that to print the struct, it needs to implement the Stringable trait, and to be able to add them to a
  DynamicVector
  They need to implement the CollectionElement trait.
- Note that traits do not yet support variables, or default implementations, but this is planned.
- Note that traits are kind of combination of Rust traits and Python ABCs

## Segue

To learn about abstract classes and how they work Python features, check out my Next Level Python Course,
link in the description.

> > show python_compat.mojo

- Explain that while you can use the fn style funcs to interface with python, this can be more verbose than necessary,
  so we can wrap our dynamic code in the def style funcs, and then handle the exceptions in the fn style funcs
  where we need too.
- Show how we can store imports in a py dict, this allows us to pass the object around in Mojos type system.
  This can help us set up our environment.
- Show how we can use def style funcs to wrap calls to Python to make the code cleaner.
- Explain that this allows us to delegate features to python that are not yet implemented in Mojo.

## Wrapping up.

Mojo is an intriguing language that shows promise for the future. It presents a unique approach by blending Python and
Rust semantics, resulting in a language that is both fast and user-friendly. This is particularly appealing to
individuals who appreciate the syntax and versatility of Python but desire enhanced performance beyond what Python can
provide. While Mojo is still in its infancy, it is a language that is worth keeping an eye on.