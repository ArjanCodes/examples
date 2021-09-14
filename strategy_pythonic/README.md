## Video outline

Just like with the Factory pattern, I'd like to take a look today at the Strategy pattern and see what other Python features we can use to establish the same thing!

## Example outline

Explain the example code (in `before`). I'm going to use Tabnine in this example, who is the sponsor of this video. Tabnine is an AI assistant that provides smart code completion in your IDE. It supports over 30 languages including Python in 15 IDEs, including VS Code and PyCharm.

Tabnine offers both a local model and a cloud model. You can choose to run Tabnine locally only and your code never leaves your machine. This also means you can use it to work offline, while ensuring maximum security and privacy.

Tabnine recently launched Tabnine for Teams, which will learn your team’s projects, preferences, and patterns, suggesting even better code completions for you and your team members.

You can get Tabnine Basic as a free extension to your IDE of choice. If you're a student, you can get Tabnine Pro for free, for more information, go to tabnine.com/students. Or you can use coupon code ARJAN20 to get a 20% discount off the Pro plan. The links are in the description of this video.

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

## Closure intro (talkinghead)

The only issue with functions is that you can't pass extra parameters, like the random seed value, because we don't have an initializer. However, you can write a function that returns a function, and then that function can have extra arguments, basically acting like an initializer. Even though these extra arguments are only passed when you call the first function, the function that it returns remembers these values. This is called a closure. Let's see what that looks like.

## Closure (screencast)

Add the closure.

An additional benefit of the closure is that you can actually define private variables here, in the function scope, and then you can't access them outside of the function (which is essentially what a closure is). You can actually still access the variables from outside the function, but it's kind of clear from the syntax that you're not supposed to do this.

In this case we're returning a single function. If you want to simulate more complex classes with multiple methods, you could return multiple functions in a tuple or a typed dictionary. But then, you might as well use a class.

## Final thoughts

So, it seems the distinction between classes and functions is not as clear cut as you'd think. In fact, classes, objects with the **call** dunder method and functions are all Callables. The syntax is just slightly different, and each of them offer different benefits. The result is that for most object-oriented patterns, you can probably mix classes, functions and objects differently to get a variety of the pattern, as I did in this video. I tried something similar a couple of weeks ago with the Factory pattern, you can check out the video here.

Hope you enjoyed this - if you did, give this video a like, and consider subscribing so you don't miss anything. Thanks for watching, take care, and see you next week.
