# 5 tips to reduce coupling

In this video I'm going to give you 5 tips to reduce coupling. The first big coupling problem I had to solve was when I did an internship in France. To this day, I'm still using the technique that I used 25 years ago. I'll tell you more about that later because I think you'll also find it very helpful.

# What is coupling?

What is coupling? Wikipedia: Coupling is the degree of interdependence between software modules; a measure of how closely connected two routines or modules are; the strength of the relationships between modules.

You can never completely remove coupling. In fact, without any coupling you'd have a bunch of completely unrelated pieces of code that won't be able to work together. Coupling is needed in some places in your code. And if you're careful about where you introduce coupling, you can really improve your code and make it much easier to maintain later on.

## Tip 1: Avoid deep inheritance hierarchies

Inheritance is one of the strongest form of coupling. In the example, if the Elasticsearch class changes, you probably need to update the subclass, but also any other class that uses your class. It's also really hard to test this class, since it is a subclass of an actual Elasticsearch class and it does a bunch of stuff in the initializer that you would then have to mock.

A better solution is to create a helper function that creates and Elasticsearch object according to your specs, and then create a find_hits function that simply takes an Elasticsearch object. Find_hits is now much easier to test as well because you can inject a mock Elasticsearch object.

## Tip 2: Separate creation from use

In the previous example you saw that the class initializer created a several other things, but at the same time, the class also uses the resources it creates. It's good practice to separate creation from use. We already did that in this example by turning the class into two functions. Here's another example (separate_creation.py). Here we have an email client that creates an SMTP server and uses it as well. If you remove the responsibility of creating the SMTP server and pass it as an argument (separate_creation_after), this now also becomes easier to test. But what's even better is that you can now introduce abstraction, and that's the next tip.

## Tip 3: Introduce abstraction

Because we separated creation from use and we injected the SMTP server into the email client, we can now use protocol classes to introduce abstraction and remove the direct dependency on SMTP (see introduce_abstraction.py, the SMTP import is now gone). Note that this is why Protocol classes are useful. We can't use ABCs in this way, because then we would have to change the SMTP class to be a subclass of an abstract class. But here, we can solve it with protocols and structural typing without having to change anything at all in the SMTP class.

## Tip 4: Avoid inappropriate intimacy

Inappropriate intimacy refers to a method in a class that has too much intimate knowledge of another class. Inappropriate intimacy is a sign of harmful, tight coupling between classes.

Example: the generate_breadcrumbs function only looks at one specific geolocation, but it has knowledge of the entire location object, which is unnecessary.

Related: law of Demeter.

## Tip 5: Introduce an intermediate data structure

If you have a piece of code that really seems tangled with lots of coupling and yo're having a hard time decreasing coupling because the code is quite complex, something that might work is to try and come up with an intermediate data structure and use that as a separation layer between the different areas of your code.

When I was doing an internship in France, I built a system that could automatically generate 3D simulations of car accidents from a brief written description provided to an insurance company. Initially, we had a hard time coming up with a solution until we decided to come up with a sort of formal representation of an accident report. This solved a lot of problems, because one team could focus on building a system that could transform a natural language description into a formal representation. And the other team (that was me :) ) could focus on turning the formal representation into an actual simulation.

And we actually did the same trick again in this project. In the formal representation, we had concepts like "overtaking", "turning left", "stopping", and so on. Because of all these different types of car movements, it was hard to build a system that could compute the car trajectories and collisions from this. So we introduced a new data structure again. We first transformed the car movements into simple trajectories: connected line segments. And then we could come up with an algorithm that, given a set of trajectories and collision points, could plan the actual collision times and precise car movements.

You can find intermediate data structures everywhere. Graphics engines use them to represent 3D scenes, Python bytecode is an intermediate data structure to help bridge the gap between the interpreter and the code runner, when you send a document to the printer, it is first converted into a lower-level format (i.e. postscript) that the printer can work with. Often intermediate data structures simplify things or throw away information, so that the lower level can work with it and doesn't become coupled to how everything works on a higher level.

Can you think of ways to introduce intermediate data structures in your own project to separate things more and reduce coupling?

I hope you enjoyed this deeper dive into coupling and that it has given you some ideas for improving your own code. Thanks for watching, take care, and see you soon!
