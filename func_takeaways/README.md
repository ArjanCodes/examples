# Intro

Python is not a functional language. In fact, everything in Python is an object! But you're doing yourself a huge disservice if you don't know at least a few things about functional programming. Because there are many things we can take from functional programming to make our code easier to maintain and easier to test. Today I'm going to cover the three most important takeaways from functional programming (or actually, from the paradigm it belongs to), and show you a few examples of how you can apply them to your own code.

# Imperative vs declarative programming

There's a fundamental difference between object-oriented programming and functional programming that goes beyond whether you're using classes with methods, or functions. In fact, OO programming and functional programming are part of two completely different paradigms.

Imperative programming – focuses on how to execute, defines control flow as statements that change a program state. A developer that writes code using this paradigm specifies the steps that the computer must take to accomplish the goal. This is sometimes referred to as algorithmic programming. Most mainstream languages, including object-oriented programming (OOP) languages such as C#, Visual Basic, C++, Java, and Python as well, were designed to primarily support imperative (procedural) programming. Object-oriented programming is a subset of imperative programming that adds classes and objects to the mix.

Declarative programming – focuses on what to execute, defines program logic, but not detailed control flow. An example of declarative programming is SQL statements. "Select \* from customers where name = arjan". We don't care how it's done (control flow), we just specify what we need. Excel is also a good example of declarative programming. You write in a cell what you want the computed value to be ("average(a2:a12)"), you don't care about how it's done. Functional programming is a specific form of declarative programming. From Wikipedia: "In computer science, functional programming is a programming paradigm where programs are constructed by applying and composing functions."

# Example introduction

Show a very simple object-oriented program (oop_v1.py).

# Takeaway 1: Minimize side effects

Because the methods in the Greeting class directly print things to the screen, they're hard to test and can't really be used by applications that don't print anything to the console but use for instance a GUI. Printing is an example of a side-effect: when you call the method, it modifies something outside of its parameters (namely, the screen - or more directly, the video memory).

In general, a side effect is when a function or method relies on, or modifies, something outside its parameters to do something. Printing something is an example, but other examples are reading from and writing to a file, interacting with a database or another service over a network, relying on an external random number generator or the current date and time.

Side effects make your code harder to reuse and make things harder to test, because you can't isolate a function or method properly. If a function doesn't have side effects and the return value is only determined by its input values (so no random number generation or relying on outside things like the current date and time), then the function is called a pure function. As opposed to functions with side effects, pure functions are easy to test and they're easier to use in different parts of your software, because there are no outside dependencies. If you want to write software that easy to work on and easy to test, take a look at your code and see whether you can turn some of your functions into pure functions. If you focus on putting all those side effects into a single place, they're much easier to manage.

In this particular case, the Greeting class prints things and it relies on the current date. If we wanted to write tests for this class, we would have to patch dates, as well as the built-in output. Which is a pain. Another way to view it is that combining for example printing with constructing the greeting message is a Single Responsibility violation: they're two different things.

So, to make the class easier to reuse, we should remove the side-effects. Let's see how what that looks like (oop_v2).

Take a look at your own code and try to identify which functions and methods have side effects. Then think about whether you can redesign it so that a bigger part of your code base doesn't have side effects anymore. It's going to make a huge difference. What also make a huge difference to me, is if you give this video a like. It helps promote the channel so others can also find this information. Dankjewel (that's Dutch).

Before I talk about the second takeaway, let's change this to using functions instead (change oop_v2 -> func_v1).

# Takeaway 2: Functions are first-class citizens

The second takeaway from functional programming is that functions are first-class citizens. They're not just groups of statements with input arguments and a return value. They are things that you can compose, deconstruct, pass to other functions, and return as a value from another function. If a function receives a function as an argument, or it returns a function as a result, it's called a higher-order function.

(modify func_v1 to func_v2 to illustrate higher order functions)
(make sure to mention strategy pattern)

Another concept from functional programming is partial function application. A partial function application means that you create a new function that is based on another function, but with some of the arguments already applied.

(modify func_v2 to func_v3 to illustrate partial function application)

I hope this shows you that functions are really flexible. You don't have to go all in on using higher-order functions and partial function application, but don't forget that these tools exist and that you don't have to stick to classes and simple functions.

# Takeaway 3: Immutability

In imperative languages like Python, variables can be accessed or changed any time you like. In declarative languages, variables are generally bound to expressions and keep a single value during their entire lifetime. For example in Excel, you specify what needs to be computed in each cell. One cell doesn't change the expression of another cell. Similarly in functional languages like Haskell, there are variables, but by default they're not mutable. Once the value is set, that's it (though Haskell does support mutable variables).

What's the advantage of having immutable variables? Well for one, it solves many multithreading problems where we might have multiple threads trying to change a single, shared variable at the same time. Another benefit is that if we have a guarantee that a variable never changes, our programs become a lot easier to understand, and they're also much easier to test.

Let's look at a few examples.

Show immutable_examples: sorting and shuffling, both in place (mutable) and immutable.

Printing the original list and the sorted list means we need to remember to make a copy. If not, the original list is gone.

If we don't change the original list, printing it is really easy. Also, because we didn't modify the original, we can now setup property tests really easy to check for example that the sorting algorithm maintains the same list length, or that the new list contains exactly the same elements as the original list. Another nice things is that sorted accepts an iterable, so you can also use it on tuples for example.

So what's the takeaway? If you notice in your code that you're changing variables all the time, try to restructure it so that this happens less often. You'll notice that your code become easier to maintain because things are more separated and it'll probably be easier to read too.

# Final thoughts

If you keep these three takeaways in mind while you're writing your code, it's going to help you automatically navigate toward better design decisions. And if you want to learn even more about applying ideas from functional programming (you can do some really cool stuff with functools in Python), watch this video next. Hope you enjoyed it, take care and see you next week.
