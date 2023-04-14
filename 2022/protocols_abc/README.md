# Introduction

Protocol classes and Abstract Base Classes in Python share a lot of similarities. But when you consider them from a software design perspective, they are quite different. Today I'm going to talk about why they're so different, give you my thoughts on both of these concepts, and show you an example where I use both, but with very different results in terms of the design.

I'm making the videos on this channel to help you understand how various programming concepts in Python work. I also talk a lot about software design principles and patterns, because I think they're extremely important to learn about if you want to become better at software development, get a better grasp on how the different pieces of a software application fit together. If you feel like you end up in a big mess as soon as your programs become more complex, I want to help you with a free software design guide. It's available at arjancodes.com/designguide. It contains my process for designing a piece of software by going through 7 steps. It's a PDF file, very practical and to the point. Just a few simple steps for you to get started quickly that'll hopefully help you out. So, get it at arjancodes.com/designguide. I also put the link in the description of this video.

# Explain the example

# ABCs

# About Protocols and Duck Typing

Protocols were introduced in Python 3.8 and behave a bit like an interface, but the difference is that you don't need to explicitly implement the protocol in a class. The result is that your class definitions become a bit shorter. ABCs rely on so-called nominal typing, meaning that if you want types to be related in some way. You have to explicitly write that down, like inheriting from an ABC. Protocols are different and rely on structural typing. This means that Python considers objects to be of matching types if their structures are the same, for example if objects have the same methods. This matches better with Python's runtime type checking system that treats objects the same if they look the same for the part that's being used at runtime. This is what's called duck typing.

# Change the example to use a protocol class

- Show that dependencies are now different: in particular, devices no longer directly inherit from the Device class

# A cool feature of protocols (talking head)

The big difference between protocols and ABCs is that as opposed to ABCs, which define the structure of the classes that inherit from them, Protocols only define what a function or method expects in terms of an interface. This reduces coupling. For example, collect_diagnostics doesn't need to know anything about the fact that devices connect and disconnect. The IOTService doesn't need to know anything about the fact that devices send status updates. So now you can define another class that just sends status updates and use that to collect diagnostics. With ABCs, you can in principle also do this, but then you'll need to use multiple inheritance, which, since inheritance is one of the strongest forms of coupling, I generally try to avoid in my code.

# Use Protocols to only define what's needed (screencast)

- Change the example to split the Protocol class in two parts.
- Show what switching on and off type checking (python.analysis.typeCheckingMode) does to both ABCs and Protocols. With type checking, ABC gives an error when you try to create an instance. Protocols give an error when you try to use a class at a place where it doesn't match the protocol.

# Final thoughts

This clearly shows the conceptual difference between Protocols and ABCs. ABCs conceptually "belong" with their subclasses. Protocols "belong" at the place where they're used.

ABCs are not obsolete because of protocols. If you want to have control over most or all of the classes implementing the interface, they can still be a very good fit. For example if you know that you're not going to define any new subclasses outside of the module containing the ABC.

Because protocols conceptually belong more at the place where they're used, they might make more sense if you expect many different classes in many different projects to use the interface and it would be unreasonable or unenforceable to expect all these external classes to explicitly inherit from an ABC.

A nice thing about Protocols is that you can even define the same protocol multiple times if you wanted to, and then the files in which these protocols are defined don't depend on each other and can still be used together, which is really cool!

However, if you're not using inheritance to define a relationship between superclass and subclass you also lose some of the advantages that inheritance offers like helpful automatic checks to inform you of mistakes such as using the wrong argument types for a method that's part of a Device subclass. You also won't be able to add convenience methods to the superclass that you can then use in a subclass. For example in the case of Device, you might want to add a convenience method that connects, runs a program and then disconnects again. With ABCs this is easy, with Protocols, you'll need to solve it differently (though that's certainly not impossible - you could for example define a function that accepts a Device and simply calls the methods).

You can use Protocols like ABCs and inherit from them if you want to. You can even use @abstractmethod with them. In that case you'll have both the static type checking that Protocols offer as well as the runtime checks with abstract methods. But arguably it's a less "pythonic" approach. And then, you'll lose the advantages of duck typing, such as being able to split the class and only define the part of the interface that you need. Doing this by the way, is called Interface Segregation and it's part of the SOLID design principles. I've talked about them in another video - there's a link at the top right.

I hope you enjoyed this video. If you did, give the video a like to help me spread the word throughout YouTube, and consider subscribing to my channel if you want to watch more of my content. Thanks for watching, take care, and see you next time!
