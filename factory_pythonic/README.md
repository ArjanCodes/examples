# Video outline

The goal of this video is to go beyond the standard patterns and show a few different ways of achieving a similar result in Python. There are a few tradeoffs though.

## Explain the basic example

This is the same Factory example I've shown before. I've used abstract base classes in this example, to stay close to the traditional design pattern. Explain how the example works. Run the code and show what happens.

## What is the factory and what is it trying to solve?

Give a short overview of what the factory patt clis (and show a UML diagram). The important design principle behind the factory is "separate creation from use". Doing this helps reducing coupling. You can create specific kinds of objects, and then have another part of your program use those objects, without it knowing any of the details. As a result, you can introduce new objects without having to change the code that uses the objects.

## Change #1: use Protocol instead of ABCs

What is a Protocol? It was introduced in Python 3.8 and it behaves a bit like an interface, but the difference is that you don't need to explicitly implement the protocol in a class. The duck typing system of Python will automatically take care of this. The result is that your class definitions become a bit shorter.

- Change the example to using Protocols instead of ABCs

Caveats of Protocols:

1. When you are creating a "subclass", you no longer have any helpful automatic check to inform you of mistakes such as using the wrong argument types for a method.
2. Since you're inheriting anymore, you can't reuse code from a superclass. For example, if you want to add a few convenience methods for processing or preparing video or audio data, you can't do that in the superclass anymore, because there is no superclass. Or, if you want a method to be there but default do nothing, this is not possible either with Protocol.

If these two things are important to you, it's better to stick with ABCs instead of Protocol.

## Change #2: Don't use Factory classes, but use a tuple

Tuples are helpful data structures that allow you to organize data. So you can use a tuple instead of a factory! Let's change the factory classes into tuples instead. Result: we can remove all the factory classes, and simply pass tuples around. This means we can do the same thing using a lot less code. Using tuples, the read_factory and do_export functions still don't need to know anything about specific video/audio exporter subclasses.

Caveats of using tuples in this way:

1. Since the video and audio exporter are directly in the tuple, you have no control over when the exporters are created. With a factory class, you can create the exporters on the fly when you call the `get_video_exporter`/`get_audio_exporter` methods. With tuples this is not possible, unless you don't store the actual exporters but creator functions instead, but then it becomes much more complicated.
2. Tuples are simply containers of objects. They don't contain any methods that you can call. If you need this, use classes instead. For example, if you want to store configuration data with a factory object, this becomes ugly quickly with tuples.
3. All combinations of video/audio exporters are now fixed in the FACTORIES constant and defined in a single place. If you have a lot of those combinations, the FACTORIES dictionary might lose cohesion.

## Final thoughts

Overall, classes and abstract base classes offer the most flexibility in terms of your design. But it comes at a price of more verbose code. Protocols integrate very well with the duck typing system, and results in shorter code, but you do lose the possibilities that inheritance offers. Tuples are a great way to quickly construct a container of objects, but don't give much control over how you access those objects and can lead to less cohesion at the place where you're creating the tuples.
