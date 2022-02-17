# Introduction

The most common use of functions in a piece of code is to group operations, and then call that function in a different place in the code. But functions are way more flexible than that. In Python, functions are objects (of type Callable). You can define types for them, pass functions as arguments to other functions. And with a package like functools, you can even call functions partially. It's better than sliced bread. And I don't even like sliced bread.

Have you noticed that in whatever country you are, the people living there think that their bread is better than in any other country? It's really weird. I mean, I live in the Netherlands so for us it's different because our bread is actually the best. But in any other country, you're basically living in a lie. How do you cope with that?

Another thing that we're really good at in the Netherlands is writing software design guides. For example this one, at arjancodes.com/designguide. It's totally free and it describes my 7 steps for designing a new piece of software, from scratch. I'm sharing that with you so you can hopefully avoid some of the mistakes I made in the past. And while you're at it, order some Dutch bread. Or, you know, keep living in your fantasy bread world. The choice is yours. Arjancodes.com/designguide. The link is also in the description of this video.

Now, I'm going to show a couple of not-so-common ways of using functions in your code. I'll do that with an example of a trading system, which relies on using different trading strategies. This is going to be like the Strategy pattern, but we're going to do some cool things with functions.

Let's dive in.

# Explain the example (screencast)

Explain the version of the code in `strategy_before.py`.

# Using functions to build the strategy pattern (talking head)

If you're not too attached to using classes, functions also provide a great way to achieve the same effect as the Strategy pattern in this example. In general, functions can replace or at least significantly simplify code that relies on classic OO design patterns. That doesn't mean that design patterns are not needed anymore. They're still useful, but don't feel obligated to use classes if a functional approach is more appropriate. Let's modify the example code to use functions instead of classes.

# Modify the code to use functions (screencast)

Change code to the version in `strategy_fn.py`.

# Limitations of the current version (talking head)

One of the issues with the current version is that there's no way to pass parameters to each of the Strategy functions. That's because the arguments should follow the expected type. For example, the TradingBot expects that the buy_strategy function takes a list of prices as an argument. But for the average buy strategy, we might want to be able to set the window size. For the minmax strategy we might want to set the price levels. In the version with classes, you could pass those parameters to the initializer. Let's look at two ways to fix this. The first is by using a closure.

# Change example to use a closure (screencast)

Change code to the version in `strategy_fn_closure.py`.

# Partial functions and Currying (talking head)

Using closures works. But it's a bit verbose. And it's not very flexible. Instead, we can use a mechanism called partial functions to solve this is in a more elegant way. A partial application (or partial function application) means that you fix a number of arguments to a function, and by doing that producing another function without those arguments. This is different from currying by the way, which is another term you may have heard from the functional programming domain. Currying is a technique where you convert a function that takes multiple arguments into a sequence of functions that each takes a single argument. What's nice about currying is that in principle, any function can be curried. That's particularly useful in theoretical computer science, because it provides a way to study functions with multiple arguments in simpler theoretical models which provide only one argument. Partial function application is more practical, and quite useful in this example, because this allows us to significantly simplify our code while making it more flexible at the same time.

# Applying partial functions (screencast)

Change code to the version in `strategy_fn_partial.py`.
