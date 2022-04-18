# Imperative vs declarative programming

Imperative programming – focuses on how to execute, defines control flow as statements that change a program state. A developer that writes code using this paradigm specifies the steps that the computer must take to accomplish the goal. This is sometimes referred to as algorithmic programming. Most mainstream languages, including object-oriented programming (OOP) languages such as C#, Visual Basic, C++, Java, and Python as well, were designed to primarily support imperative (procedural) programming. Object-oriented programming is a subset of imperative programming that adds classes and objects to the mix.

Declarative programming – focuses on what to execute, defines program logic, but not detailed control flow. An example of declarative programming is SQL statements. "Select \* from customers where name = arjan". We don't care how it's done (control flow), we just specify what we need. Excel is also a good example of declarative programming. You write in a cell what you want the computed value to be ("average(a2:a12)"), you don't care about how it's done. Functional programming is a specific form of declarative programming. A functional approach involves composing the problem as a set of functions to be executed.

# Tips for OOP done well

1. Make your classes either behavior-focused (mainly acting as a group of methods/behavior), or data-focused (representing a structured collection of data with not too many methods in the class).

2. The more you use inheritance, the more complication you add to your program. Mixins make things even worse because you inherit from multiple classes (and there are a bunch of other reasons why using mixins is a really bad idea). I generally only use inheritance in the sense that I define interfaces using either ABCs or Protocol classes and then inherit from the ABCs (Protocols don't have an inheritance relationship). The classic design patterns follow this same principle: very lightweight inheritance, mainly rely on composition.

3. Use dependency injection to make connections between objects (composition). In general I don't let objects create other objects, because it leads to code that's harder to test.
