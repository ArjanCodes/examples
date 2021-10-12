# Introduction

Protocol classes and Abstract Base Classes in Python share a lot of similarities. But when you consider them from a software design perspective, they are quite different. Today I'm going to talk about why they're so different, give you my thoughts on both of these concepts, and show you an example where I use both, but with very different results in terms of the design.

I'm making the videos on this channel to help you understand how various programming concepts in Python work. I also talk a lot about software design principles and patterns, because I think they're extremely important to learn about if you want to become better at software development, get a better grasp on how the different pieces of a software application fit together. If you feel like you end up in a big mess as soon as your programs become more complex, I want to help you with a free software design guide. It's available at arjancodes.com/designguide. It contains my process for designing a piece of software by going through 7 steps. It's a PDF file, very practical and to the point. Just a few simple steps for you to get started quickly that'll hopefully help you out. So, get it at arjancodes.com/designguide. I also put the link in the description of this video.

# Explain the example

# ABCs

# About Protocols and Duck Typing

Protocols were introduced in Python 3.8 and behave a bit like an interface, but the difference is that you don't need to explicitly implement the protocol in a class. The result is that your class definitions become a bit shorter. ABCs rely on so-called nominal typing, meaning that if you want types to be related in some way. You have to explicitly write that down, like inheriting from an ABC. Protocols are different and rely on structural typing. This means that Python considers objects to be of matching types if their structures are the same, for example if objects have the same methods. This matches better with Python's runtime type checking system that treats objects the same if they look the same for the part that's being used at runtime. This is what's called duck typing.

# Change the example to use a protocol class

- Show that dependencies are now different: in particular, devices no longer directly inherit from

# A cool feature of protocols (talking head)

The big difference between protocols and ABCs is that as opposed to ABCs, which define the structure of the classes that inherit from them, Protocols only define what a function or method expects in terms of an interface. This reduces coupling. For example, collect_diagnostics doesn't need to know anything about the fact that devices connect and disconnect. The IOTService doesn't need to know anything about the fact that devices send status updates. So now you can define another class that just sends status updates and use that to collect diagnostics. With ABCs, this isn't possible.

This clearly shows the conceptual difference between Protocols and ABCs. ABCs "belong" together with their subclasses. Protocols "belong" at the place where they're used. When you use Protocols, you can even define the same protocol multiple times if you wanted to, and then the files in which these protocols are defined don't depend on each other and can still be used together.

# Use Protocols to only define what's needed (screencast)

- Change the example to split the Protocol class in two parts.

# Final thoughts
