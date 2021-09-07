# Video outline

[talkinghead] Design patterns were conceived in the 90s, when Object-oriented programming was extremely popular. So naturally design patterns rely on classes and inheritance. But, programming languages have evolved. Python not only has classes, but also tuples, dictionaries, Protocol classes and dataclasses.

What I'm going to do in today's video is take one design pattern, the Factory, strip it down completely until we arrive at the design principles that are behind the pattern. And then, I'm going to investigate whether it's possible to achieve the same thing, but better, using more modern constructs of Python instead of the traditional classes. Spoiler: it's possible, though there are a few tradeoffs.

Before we start, I have a free guide for you to help you make better design decisions. You can get it at arjancodes.com/designguide. I've tried to keep the guide short and to the point, so you can get the information quickly and apply it immediately to what you're doing. So, arjancodes.com/designguide.

Now let's take a look at the example.

## Explain the basic example

[screencast] This is the same Factory example I've shown before. I've used abstract base classes in this example, to stay close to the traditional design pattern. Explain how the example works. Run the code and show what happens.

Now, let's look at three variations of the Factory pattern.

## What is the factory and what is it trying to solve?

[talkinghead] Give a short overview of what the factory patt clis (and show a UML diagram). The most important design principle behind the factory is "separate creation from use". Doing this helps reducing coupling. You can create specific kinds of objects, and then have another part of your program use those objects, without it knowing any of the details. As a result, you can introduce new objects without having to change the code that uses the objects.

A related, more generic principle is Single Responsibility principle. We don't want the responsibility of creating the thing and using the thing to be in the same place.

Finally, we have Open-Closed: being able to extend the code that uses the exporters in this case by introducing new exporters. We don't have to change the original code for that, we simply create a new factory.

## Change #1: use Protocol instead of ABCs

[screencast] What is a Protocol? It was introduced in Python 3.8 and it behaves a bit like an interface, but the difference is that you don't need to explicitly implement the protocol in a class. The result is that your class definitions become a bit shorter. ABCs rely on so-called nominal typing, meaning that if you want types to be related in some way. You have to explicitly write that down, like inheriting from an ABC. Protocols are different and rely on structural typing. This means that Python considers objects to be of matching types if their structures are the same, for example if objects have the same methods. This matches better with Python's runtime type checking system that treats objects the same if they look the same for the part that's being used at runtime. This is what's called duck typing. So let's change the example and see what the effect is.

- Change the example to using Protocols instead of ABCs.

[talkinghead] - Overall, I think in Python, protocols are the way to go most of the time. Until recently, I've relied on ABCs in a large part for explaining the design patterns, but as you can see, Protocols work just as well and offer more flexibility.

Caveats:

1. If you're not using inheritance like I'm doing here you also lose some of the advantages that inheritance offers like helpful automatic checks to inform you of mistakes such as using the wrong argument types for a method, or being able to add convenience methods to the superclass that you use in a subclass.
2. You can use Protocols like ABCs and inherit from them. You can even use @abstractmethod. In that case you'll have both the static type checking that Protocols offer as well as the runtime checks with abstract methods. But arguably it's a less "pythonic" approach.

## Change #2: Don't use Factory classes, but use a tuple

[screencast] Tuples are helpful data structures that allow you to organize data. So you can use a tuple instead of a factory! Let's change the factory classes into tuples instead. Result: we can remove all the factory classes, and simply pass tuples around. This means we can do the same thing using a lot less code. Using tuples, the read_factory and do_export functions still don't need to know anything about specific video/audio exporter subclasses.

[talkinghead] Caveats of using tuples in this way:

1. Tuples are simply containers of objects. They don't contain any methods that you can call. If you need this, use classes instead. For example, if you want to store configuration data with a factory object, this becomes ugly quickly with tuples.
2. All combinations of video/audio exporters are now fixed in the FACTORIES constant and defined in a single place. If you have a lot of those combinations, the FACTORIES dictionary might lose cohesion.
3. You need to remember the order of the exporters everywhere (video first, then audio). It's not a big issue, but one more thing that can potentially go wrong. You could use named tuples, but another option is using dataclasses in combination with the **call** dunder method.

## Change #3: Use dataclasses with the **call** dunder method

[screencast] Create a media exporter dataclass, and a factory data class + add **call** method to easily define them.

1. Overall, I find this a nice, clean approach that combines Python features to have a factory-like pattern.
2. The advantage of named tuples over dataclasses though is that they're lighter weight (as in, use less memory and have faster element access), and they're immutable. If that's not important, personally I'd go for dataclasses instead.

## Final thoughts

[talkinghead] Overall, protocols integrate very well with Python's duck typing system, and results in shorter code than using ABCs and inheritance. Tuples are a great way to quickly construct a container of objects, but you expose the structure of your factory to the outside. They can lead to less cohesion at the place where you're creating the tuples. Data classes combined with the **call** dunder methods are a nice Pythonic approach to factories, but dataclasses do have some overhead in terms of memory usage and they're slower in terms of accessing the elements than tuples.

Let me know in the comments which of these versions you prefer. If you have another suggestion for achieving this, please share, I'd be very curious to hear more. That's it for today, thanks for watching, take care and see you next time.
