## Introduction

Rust is quickly making a name for itself as a speedy and approachable programming language.
It unique approach to type safety, memory management and exception handling ake it a powerhouse for performance critical
applications.

Given the many similarities between Python and Rusts syntax, the ability to bind Rust to Python modules and its high
performance, it makes for a perfect language for Pythonistas’ to pick up.

So, let me show you some of the cool features that Rust brings to the table, and how they differ from Python.

## Short overview of key differences

| Feature           | Python                                    | Rust                                     |
|-------------------|-------------------------------------------|------------------------------------------|
| Typing            | Dynamic typing                            | Static Strong typing                     |
| Memory Management | Automatic garbage collection              | Manual memory management (ownership)     |
| Concurrency       | Global Interpreter Lock (GIL) for CPython | No GIL, supports concurrency safely      |
| Error Handling    | Exception-based                           | Result and Option types for control flow |
| Syntax            | Clean and concise syntax                  | Strict and explicit syntax               |
| Performance       | Interpreted, slower execution             | Compiled language, emphasizes speed      |
| Learning Curve    | Beginner-friendly                         | Steeper learning curve                   |

- Show example of Rusts hello world vs Pythons hello world

> > rust/hello_world.rs

on linux
`rustc main.rs./main`

or on windows
`rustc main.rs./main.exe`

> > python/hello_world.py

`python3 hello.py`  on linux

`python hello.py` on windows

---

- Show python class example and rust struct + impl example.

> > python/user.py class section

> > rust/user.rs struct/impl section

- Demonstrate how there are syntactic similarities between the two languages, but also distinct differences, such as
  the & ref.
- Explain how Rust is more verbose, but more explicit.
- Explain that python is mainly OOP, while Rust is mainly functional.
- Explain that rust makes strong use of the monadic pattern.
- Explain how with Python you can define methods in the class body,
  but in rust you have to define them in the impl block.
- Explain that in Rust all references are immutable by default, and that you have to explicitly define when you are
  working with a mutable reference.

> > rust/user.rs main section

- Explain that in rust there is no None type, and that you have to use the Option type instead.
- Explain that in python exception handling is done with try/except, and in rust it is done with the Result type.
- Explain that in rust you have to explicitly define the types for a functions arguments and return.
  this is due to the fact that rust is strongly typed, and like most compiled languages, the compiler needs to know the
  types ahead of time

> > rust/user.rs function section

### Show the differences between an ABC and a trait

> > python/iot.py ABC section

> > rust/iot.rs trait section

- Explain how that in python, we are utilizing inheritance to define an interface, which will later be subclassed.
  This sometime can cause clashes with naming, and while python can make use of multiple inheritance, it can cause
  problems with the MRO (method resolution order).
- In Rust, we are using a trait, which is similar in many ways to an interface, but it is more powerful. It can be
  implemented on any type as long as that type is local to the crate. This also deals with the problem of naming
  clashes, and it is more explicit.
- Explain how traits have to be implemented on every type you with to use it on.
- Explain that in rust, you can implement traits on types that are not local to the crate and vise versa,
  but you have to use the orphan rule, which states that either the trait or the type must be local to the crate.
- Explain that there are other key differences, like how rust uses enums and attributes.

> > python/iot.py connection section

> > rust/iot.rs connection section

- Explain that rust enums are more powerful than python enums, and that they can hold data which means they not only
  hold their state, but also their data. This is useful for things like state machines, which can help reduce errors in
  code.
- Explain that rust enums can also have methods, which is useful for encapsulating logic, and working with their data.
- Explain that this enum behaviour is the cornerstone of how rust deals with errors, and other various monadic behavior.
- Explain attributes, and how they are used to define metadata about a function, struct, enum, etc, or run procedural
  macros that can do things such as automatically implement traits on a struct.

### Explain macros in rust

> > rust/iot.rs macro section

- Explain that rust has a powerful macro system and it can help cut down on code repetition,
  but they can make code confusing if overused.

### more on rust

- Rust, being a functional language, better suits the railroad style of programming, as there are usually two distinct
  paths the "happy path" and the "error path". This is why rust has the Result type, which values can be either Ok or
  Err.
- Rust uses a lot of chaining methods, such as mapping, filtering, and folding. This is why rust has the Option type,
  to handle cases where there is no, or a method failed etc.
- Python on the other hand is more suited to the "duck typing" style of programming, where you don't care what type you
  are working with and while this makes it much easier and faster to write code, it can lead to errors that are hard to
  debug. It is also much easier to misuse python code, as it does not carry the same type safety as rust.
- Give brief explanation that rust can interface with python using modules such as pyo3 and cffi and this could be a
  potential benefit to learning rust, as it can be used to speed up python code, so it’s possible to marry the qualities
  of both languages to design even better software.

### Final thoughts

- Rust is a powerful language that is fast, typesafe and while verbose is still pretty easy to read and write.
- Python on the other hand is powerful due to its simplicity, dynamic typing and ease of use.
- Rust has a growing ecosystem of libraries much akin to pypi, and via rust bindings, many of these can be used
  alongside python.