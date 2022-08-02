# 5 tips to reduce coupling

## Tip 1: inheritance is the strongest form of coupling

## Tip 2: separate creation from use

## Tip 3: introduce abstraction

## Tip 4: inappropriate intimacy

Inappropriate intimacy refers to a method in a class that has too much intimate knowledge of another class. Inappropriate intimacy is a sign of harmful, tight coupling between classes. Let's say that we have a business logic class that calls an instance of class DataServer1 to get the data it needs for its business-logic processing. Figure 2 shows an example. In this case, the Process method has to know a lot of the inner workings of DataServer1 and a bit about the SqlDataReader class.

Related: law of Demeter.

## Tip 5: increase cohesion

From Steve McConnell's "Code Complete": "Cohesion refers to how closely all the routines in a class or all the code in a routine support a central purpose. Classes that contain strongly related functionality are described as having strong cohesion, and the heuristic goal is to make cohesion as strong as possible. Cohesion is a useful tool for managing complexity because the more code in a class supports a central purpose, the more easily your brain can remember everything the code does."

In general it is neither advisable nor possible to create such maximally cohesive classes; on the other hand, we would like cohesion to be high. When cohesion is high, it means that the methods and variables of the class are co-dependent and hang together as a logical whole."

also, there is a principle based on the heuristic of high cohesion, named Single Responsibility Principle (the S from SOLID). A class should only do what it is supposed to do, and does it fully.

Can we talk about cohesion when we don't write classes but use only functions and modules. If you're a purist, no. But I'm not a purist, so I think cohesion and the single responsibiity principle also make sense when you write modules and functions.

From Clean Code: "Classes should have a small number of instance variables. Each of the methods of a class should manipulate one or more of those variables. In general the more variables a method manipulates the more cohesive that method is to its class. A class in which each variable is used by each method is maximally cohesive.

https://stackoverflow.com/questions/10830135/what-is-high-cohesion-and-how-to-use-it-make-it
