# 5 tips to reduce coupling

In this video I'm going to give you 5 tips to reduce coupling. The first big coupling problem I had to solve was almost 25 years ago, when I did an internship in France as part of my computer science studies. The technique I used to solve that problem and that I'll also talk about in this video is one that I still use today because it's really effective. If you've never used this technique, you're missing out on a really powerful way to reduce coupling.

Reducing coupling in your code is a great way to improve your design, but that's only part of the puzzle. You need to be able to detect coupling issues before you can tackle them. And this is not just for coupling: in general you need to understand a problem before you can fix it. Being able to diagnose code quickly is - in my opinion - one of the most important skills you should have as a software developer. That's why I've created a Code Diagnosis workshop where I teach you the most important things to look for when you want to quickly identify design problems in your code. It's based on my own experience reviewing code for more than two decades and trying to make that process as efficient and effective at possible. The workshop will help you focus on what matters, you'll be able to do code reviews much faster, and the best thing: it's free. You can sign up at arjan.codes/diagnosis. It's in-depth, contains a ton of useful advice and practical code examples. I thought about offering this as a paid course actually, because there's a ton of value, but I want to give it to you for free. So check it out, arjan.codes/diagnosis, the link is also in the description.

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

There are also some design patterns that can help with separating creation from use and introducing abstract, such as the Abstract Factory. If you want to learn more about that, I've put a video at the top explaining the pattern in more detail.

## Tip 4: Avoid inappropriate intimacy

Inappropriate intimacy refers to a method in a class that has too much intimate knowledge of another class. Inappropriate intimacy is a sign of harmful, tight coupling between classes.

Example: the generate_breadcrumbs function only looks at one specific geolocation, but it has knowledge of the entire location object, which is unnecessary.

Related: law of Demeter.

## Tip 5: Introduce an intermediate data structure

Sometimes, you have a piece of code that seems really tangled with lots of coupling and you're having a hard time decreasing coupling because the code is quite complex. In this case, it might be very hard to apply the things I mentioned earlier in this video. Something that can work really well in this case is to introduce an intermediate data structure and use that as a separation layer between the different areas of your code.

When I was doing an internship in France, I built a system that could automatically generate 3D simulations of car accidents from a brief written description provided by an insurance company. Initially, we had a hard time coming up with a solution. I mean, there are lots of connections between different verbs, actions, types of collisions and how you express that in natural language. We had a breakthrough when we decided to come up with a sort of formal representation of an accident report. This solved a lot of problems, because one team could focus on building a system that could transform a natural language description into this formal representation. And the other team (that was me :) ) could focus on turning the formal representation into an actual 3D simulation.

And we actually used this trick again in the same project. In the formal representation, we had concepts like "overtaking", "turning left", "stopping", and so on. Because of all these different types of car movements, it was hard to build a system that could compute the car trajectories and collisions from this. So we introduced a new data structure again. We first transformed the car movements into simple trajectories: connected line segments. And then we could come up with an algorithm that, given a set of trajectories and collision points, could plan the actual collisions and precise car movements.

You can find intermediate data structures everywhere. Graphics engines use them to represent 3D scenes, Python bytecode is an intermediate data structure to help bridge the gap between the interpreter and the code runner, when you send a document to the printer, it is first converted into a lower-level format (i.e. postscript) that the printer can work with. Often intermediate data structures simplify things or throw away information, so that the lower level can work with it and doesn't become coupled to how everything works on a higher level.

Can you think of ways to introduce intermediate data structures in your own project to separate things more and reduce coupling?

I hope you enjoyed this deeper dive into coupling and that it has given you some ideas for improving your own code. If you want to get more practical tips for improving your code quality, check out this video where I dive deeper into how to do object-oriented programming well. Give this video a like, consider subscribing to my channel if you want to learn more about software design and development. Thanks for watching and take care!
