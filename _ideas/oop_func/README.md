# Intro

In this video, I'd like to go through a few varieties of the same programming and move from a purely OOP solutions to a purely functional solution and look at the differences.

When I started studying CS, in 1995, Java just appeared on the scene. It wasn't yet part of my curriculum in my first and second year (I learned Modula-2 and C++), but after that, the entire education sector changed to Java. In some sense, Java encapsulates the worst of OOP. It's verbose, you can't not use a class in your program. So it invites you to write really complex programs and structures. It was quickly adopted by businesses to write very complex designs with deep inheritance hierarchies, very long class names, and overly complex software structures fed by complex design processes involving many stakeholders (Waterfall, Rational Unified Process). I still see some teachers in CS doing this with Java and I think it's for a big part responsible for the hatred against OOP.

Myself I've moved more towards functional programming lately. This is also in part because I've been developing a lot of software using REact and Typescript. Typescript has great support for functional programming, and React relies on a lot on functional components. So moving to functional programming came quite naturally to me.

You may have seen part of this shift in my videos over the last year. It doesn't mean I don't like OOP though. Used carefully, classes can really help you write cleaner, more readable code. And in Python, we don't have to choose between OOP and functional. We can use a combination of both.

# Imperative vs declarative programming

Imperative programming – focuses on how to execute, defines control flow as statements that change a program state. A developer that writes code using this paradigm specifies the steps that the computer must take to accomplish the goal. This is sometimes referred to as algorithmic programming. Most mainstream languages, including object-oriented programming (OOP) languages such as C#, Visual Basic, C++, Java, and Python as well, were designed to primarily support imperative (procedural) programming. Object-oriented programming is a subset of imperative programming that adds classes and objects to the mix.

Declarative programming – focuses on what to execute, defines program logic, but not detailed control flow. An example of declarative programming is SQL statements. "Select \* from customers where name = arjan". We don't care how it's done (control flow), we just specify what we need. Excel is also a good example of declarative programming. You write in a cell what you want the computed value to be ("average(a2:a12)"), you don't care about how it's done. Functional programming is a specific form of declarative programming. A functional approach involves composing the problem as a set of functions to be executed.

# Basic OOP example

# Remove the printing part

Because the methods in the Greeting class directly print things to the screen, they're hard to test and can't really be used by applications that don't print anything to the console but use for instance a GUI. Let's put the printing part in a single place (the main function), so we can replace it with something else more easily.

# A functional approach

# Using pure functions only

Here's an approach that uses pure functions only (= functions without side effects)

# Hardcore functional programming: partial function application and higher order functions

Higher-order functions: functions that receive a function as a argument or return a function as a result

Partial function application: create a function that is based on another function, but with some arguments already applied.

# Tips for OOP done well

There's no need to only use OOP or only use hardcore functional programming. Use whatever results in the most readable code. And that's certainly not always purely functional programming with no state whatsoever.

If you use OOP, here are a few tips to keep things simple and clean:

1. Make your classes either behavior-focused (mainly acting as a group of methods/behavior), or data-focused (representing a structured collection of data with not too many methods in the class).

2. The more you use inheritance, the more complication you add to your program. Mixins make things even worse because you inherit from multiple classes (and there are a bunch of other reasons why using mixins is a really bad idea). I generally only use inheritance in the sense that I define interfaces using either ABCs or Protocol classes and then inherit from the ABCs (Protocols don't have an inheritance relationship). The classic design patterns follow this same principle: very lightweight inheritance, mainly rely on composition.

3. Use dependency injection to make connections between objects (composition). In general I don't let objects create other objects, because it leads to code that's harder to test.
