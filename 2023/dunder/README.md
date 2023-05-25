- Today I want to talk about dunder methods, when to use them, and when to avoid them.
- We’ve all seen dunder methods before: the most common one is the dunder init method to initialize a class.
- They offer unparalleled flexibility: they allow you to basically change everything that Python does under the hood.
- If you’re not careful and you use them in the wrong way, it leads to really confusing code and makes your programs hard to understand.

## The Python data model

- Let's take a step back and explore the history behind the Python data model.
- Python, as a language, was created with a strong emphasis on simplicity and readability.
- Guido van Rossum, the creator of Python, envisioned a language that would be easy to understand and express ideas in a concise manner.
- To achieve this vision, Python embraces the concept that "everything is an object." This means that every piece of data in Python, whether it's a number, a string, a list, or even a function, is represented as an object. This fundamental design choice led to the development of the Python data model.
- So, what exactly is the Python data model? At its core, the data model defines the rules and protocols that govern how objects behave in Python. It provides a standard interface and a set of protocols that objects can follow, enabling them to work seamlessly with built-in Python features.
- Central to the Python data model are the dunder methods. These special methods, denoted by double underscores before and after their names, allow us to define how our objects interact with various operations and built-in functions. They give us the power to customize the behavior of our objects and make Python a flexible and extensible language.
- Dunder methods are like hooks into the Python interpreter, enabling us to define operations such as object creation, object representation, attribute access, iteration, and more.
- Typically, dunder methods are not invoked directly by you, making it look like they are called by magic. That is why dunder methods are also referred to as “magic methods”.
- The Python data model has evolved over time, with each version of Python introducing new dunder methods and expanding the capabilities of the language.

Like I said before, overriding dunder (double underscore) methods can be powerful and useful, as long as you’re careful. So, here are some guidelines for when to override dunder methods and when to avoid them:

## When to override dunder methods

1. Implementing custom behavior: Dunder methods allow you to define custom behavior for your objects. If you want your object to respond to specific operations or have specific behavior when used in certain contexts, overriding the corresponding dunder method is appropriate. For example, you might override **`__str__`** to provide a human-readable representation of your object or **`__getitem__`** to enable indexing or slicing on your custom data structure.
   1. See example _p1_
2. Emulating built-in types: Dunder methods can be used to emulate the behavior of built-in types such as lists, dictionaries, or strings. If you're creating a custom object that should behave similarly to a built-in type, overriding relevant dunder methods like **`__len__`**, **`__iter__`**, or **`__contains__`** can be helpful.
   1. See example _p2_
3. Operator overloading: Dunder methods enable operator overloading in Python. By overriding methods like **`__add__`**, **`__eq__`**, or **`__lt__`**, you can define custom behavior for operators like **`+`**, **`==`**, or **`<`** when applied to your objects. This can make your code more expressive and intuitive.
   1. See example _p3_
4. Context management: If your object needs to set up and tear down resources in a specific context, such as opening and closing a file, you can use the **`__enter__`** and **`__exit__`** methods to implement the context management protocol. This allows you to use your object with the **`with`** statement. Even though you can also use the contextmanager decorator + a generator function to do this.
   1. See example _p4_

## When to not override dunder methods

1. Unnecessary complexity: Overriding dunder methods should be done with caution. If the default behavior of the base class or the built-in behavior of Python already meets your needs, there might be no need to override a dunder method. Adding unnecessary complexity to your codebase can make it harder to understand and maintain.
   1. Instead of using a class with a call dunder method, using functions is much simpler (see example _c1_)
2. Violating the principle of least astonishment: Dunder methods should follow intuitive and expected behavior. If your implementation significantly deviates from the typical behavior associated with a dunder method, it can lead to confusion and make your code harder to reason about. Stick to conventions and established patterns unless you have a compelling reason to deviate from them.
   1. Overriding the new dunder method seems like a cool “trick”, but it’s actually really confusing since creating an object now returns an object of a different type (see example _c2_)
3. Performance considerations: Overriding certain dunder methods can impact the performance of your code. For example, overriding **`__eq__`** inappropriately can lead to unexpected behavior in sets or dictionaries. Consider the performance implications and potential trade-offs before overriding these methods.
   1. Using a hash function to make comparison easier impacts performance by over a factor 10! (see example _c3_)
4. Code readability and maintainability: Overuse or misuse of dunder methods can make your code less readable and harder to maintain. Be mindful of the complexity you introduce when overriding dunder methods and ensure that it improves the clarity and maintainability of your code. Always ask yourself the question whether you really need to override the method.
   1. I don’t have a specific example for this one - it’s more generic advice. Reviewers: if you have a specific idea to demonstrate this, let me know!

## Final thoughts

I hope this video gave you some food for thought about how to deal responsibly with the flexibility that Python offers. Another area where Python is really flexible is that it allows you do setup your code in an object-oriented was as well as in a functional way. But it’s important to pick the right approach for the circumstance. If you want to learn how to do that, watch this video next. Thanks for watching and see you next week!
