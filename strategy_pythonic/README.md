## Video outline

Just like with the Factory pattern, I'd like to take a look today at the Strategy pattern and see what other Python features we can use to establish the same thing!

## Example outline

Explain the example code (in `before`).

## The strategy pattern (talking head)

The strategy pattern allows you to inject behavior into an application, without that code knowing exactly what the behavior does. Here's a class diagram of the pattern. It relies on an interface (basically the signature of the Strategy function) to break up an application and reduce coupling. The idea is that the interface specifies a class with a method. You then create subclasses of that class and inject a strategy instance into the part of the program that calls the method, without knowing which version of it is calling. Let's first look at how to apply this classic strategy pattern to our example

## Classic strategy pattern (screencast)

Refactor the code so that it now uses the strategy pattern (see the `classic` folder).

## Protocols (Screencast)

Replace the abstract base classes by protocol classes. This considerably simplifies the code.

## Dunder method (screencast)

Similar to what we did with the Factory pattern, we can also use a class with a `__call__` dunder method.

## Functions (screencast)

Here's another way to do it: using functions! The interesting thing is that actually, the class with the `__call__` dunder method is compatible with the Callable typing. So this version you can still use with classes as well and you don't need to change the type. The other way around is true as well. You can use the class + call definition to define the type and then a regular function also fits the bill! The cool thing is that you can now also replace the Callable type with the class type + dunder method. No more Callable! Arjan happy!

## Function generator intro (talkinghead)

The only issue with functions is that you can't pass extra parameters, like the random seed value, because we don't have an initializer. However, you can write a function that returns a function, and then that function can have extra arguments, basically acting like an initializer. Let's see what that looks like.

## Function generator (screencast)

Add the function generator.

An additional benefit of the function generator is that you can actually define true private variables here, in the function scope, and then you can't access them outside of the function. Classes don't have this feature. Now, in this case we're returning a single function. If you want to simulate more complex classes with multiple methods, you could return multiple functions in a tuple or a typed dictionary. But then, you might as well use a class.

## Final thoughts

So, it seems the distinction between classes and functions is not as clear cut as you'd think. Classes can behave like functions using the call dunder method. Functions can behave like classes, with an initializer and private instance variables. For most design patterns, either of these approaches works. Typing/protocols are there to define the contracts: what are methods or functions expecting. Both classes and functions are containers of behavior, and are more similar than you think. If you need state, or several methods working with that state, probably classes are a simpler option. But true private variables don't exist. You can also use a function, but then if you want to add state, or having multiple functions do something with that state, it becomes complicated. I am intrigued though by the interchangeability of class types with the dunder call method and the Callable type. I really don't like the Callable type syntax. Should I use classes with the dunder call method from now on? Let me know what you think in the comments.

Hope you enjoyed this - if you did, give this video a like, and consider subscribing so you don't miss anything. Thanks for watching, take care, and see you next week.
