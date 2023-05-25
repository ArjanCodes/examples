- One of the best ways I found to make coding easier and faster is by being strict!
- I don’t mean that you should be a pain in the neck for your fellow team mates: “I only accept code where the number of lines in a file is a fibonacci number”
- I’m going to show you 3 mistakes I see developers commonly make because they’re not strict enough. I’ll also show you the consequences of these mistakes.
- If you’re not strict you’ll write more code that necessary, and on top of that, your code will be more complex than needed. And if that’s a pattern that happens throughout a bigger code base, well, you’re in trouble.
- So let’s dive straight in, before it’s too late!

## Being strict

- What I mean by being strict is that you’re mindful of what kind of data your functions or methods work with as well as that you’re precise in defining the scope of what your functions or methods actually need.
- Mistake 1: Being precise when defining what arguments a function expects
  - only ask for what you actually need, nothing more (example 1)
    - consequence: function is highly coupled to a data structure (Geolocation) while that’s not needed, that makes reusing the function harder
  - if you add type annotations, make sure you they are appropriate (example 2)
    - for example, don’t use list if you can use Iterable & don’t use a type like str if Sized is enough
    - consequence: you’re artificially limiting yourself, `count` can now only be used with lists of strings, and not with tuples of lists for example
- Mistake 2: Being strict in terms of the type of data you can handle
  - only accept one type for arguments. For example, only accept strings, not numbers or strings or booleans or dictionaries, etc (example 3)
    - consequence: a) if you write tests, you need to now cover all of these cases, and b) refactoring the code later could be hard because you won’t be able to deal with all the cases anymore, or you might introduce bugs because of too much allowed flexibility
- Mistake 3: Being strict in terms of the kind of things your function or method returns
  - return one specific thing, if something is wrong, use an exception (example 3)
    - consequence: whenever you call the function, you need to take into account the possibility of getting a different result, so it leads to more code (and probably more duplication as well since you need to do that everywhere)
  - also share tip on defining custom Exception classes with data

## Final thoughts

Here are a few other things you can do to keep your code simple.

1. Use appropriate data structures and algorithms: Selecting the right data structures and algorithms can significantly reduce the amount of code you need to write. Choose efficient data structures that fit your problem domain and leverage algorithmic techniques to optimize your code's performance.
2. Avoid premature optimization: Don't overcomplicate your code by trying to optimize every small aspect from the beginning. Focus on writing clean, maintainable code first, and then profile and optimize only the critical parts if necessary. Premature optimization often leads to convoluted and hard-to-maintain code.
3. Leverage existing libraries and frameworks: Before reinventing the wheel, explore available libraries and frameworks that can solve common programming challenges. Reusing well-tested and widely adopted solutions can save you time and effort, reducing the amount of code you need to write.
4. Refactor and simplify code regularly: As you gain a deeper understanding of the problem domain and improve your skills, revisit your codebase regularly to identify opportunities for refactoring and simplification. Eliminate unnecessary complexity, reduce code redundancy, and improve overall code quality.

Hope you enjoyed this video.
