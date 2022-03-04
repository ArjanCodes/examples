# What is a dataclass and how is it different from a regular class?

- Mainly aimed at more data-oriented classes (i.e. Points and Vectors vs Button or PaymentService)
- Adds convenient mechanisms such as easier comparison, string representation, and easier definition and initialization
- Show example: PersonNoDataClass vs Person

# Usage of dataclasses

Several reasons for me to use dataclasses are:

1. It's much shorter to define a class with a couple of attributes than with a regular class
2. I find it clearer to see what data is contained within a class if it's a dataclass
3. Already having a reasonable implementation for printing and initializing an object is very useful

One thing I don't like about dataclasses is that they 'abuse' the concept of a class variable to represent instance variables. It's confusing, especially to beginners. And if you forget the @dataclass decorator, you end up with a bunch of class variables and you may not even realize it.

# Different things you can do with a dataclass

- default values for fields
  - add an active field to Person set to True
- default factory for lists/dicts
  - initialize a list of email addresses
- using a function for a default factory
  - add an id field with a function to generate the id
- exclude attributes from the initializer
  - add an init=False to the id field so we can't set it with the initializer
- Post init
  - Show example of adding a search string after initialization that uses the other instance variables
- private attributes of a class
  - Make the search string "private", and remove it from the initializer
- exclude certain attributes from the representation
  - Exclude the search string using the option repr=False

# Recent additions to dataclasses (in 3.10)

## kw_only

If true (the default value is False), then all fields will be marked as keyword-only. The **init**() parameter generated from a keyword-only field must be specified with a keyword when **init**() is called.

## match_args

Default True. This generates the match_args dunder variable. This contains a list of strings, each value represents a property you can access when you do structural pattern matching (which is a new feature in 3.10)

## slots

Normally, objects store their attributes in a dictionary (held by the dunder dict variable). You can change this to use the slots dunder variable instead, which has faster access (show example that illustrates this - I measured about 20-25% improvement). Slots also use less memory.

Most important caveat with **slots** is multiple inheritance. When more than 1 superclass has the dunder slots defined, the code doesn't run (see the PersonEmployee class in slots).

So, that's yet another reason to avoid multiple inheritance. I'm pretty opinionated about multiple inheritance (and mixins). I talk about that in my course at length. I won't go into too much detail in this video, but my general advice is to not use multiple inheritance or mixins at all.

I get why the default is that slots are not used. Setting slots as default would break a lot of existing Python code. However, I think it would be nice if a 'strict' mode was added to Python that limits a couple of things: slots by default instead of dict, multiple inheritance is not allowed, some of the dunder methods can't be used anymore like **init_subclass** or **set_attr**, perhaps stricter type enforcement or exception handling as well. The interpreter can then make more assumptions about what the script does and thus improve performance and reliability. With JavaScript something similar was done by introducing strict mode that turns some of the silent errors into actually throwing errors, and imposes some limitations on global use, this in functions, and variable names.
