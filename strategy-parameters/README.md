## About this video

This video is about how to use the Strategy pattern where each strategy has different parameters

## Video outline

- In this video, I revisit the Strategy design pattern, and I'll talk about an issue that a lot of people have when using it. How do you model strategies with different parameter types and values? I'll show three different ways of doing this. But only one of them is a good solution.

- Give an overview of the example (trading bot with different trading strategies).

- The issue with the example is that each strategy currently has hard-coded parameters. The average trading strategy has a fixed window size. The min-max trading strategy has fixed min and max prices.

- First solution: add \*\*kwargs to the strategy function and use that to pass parameters. This works, but a) you loose typing information since kwargs is an arbitrary dict of floats and b) not all arguments are floats so you have to do type casting to int for the window size, or use Union types, which is ugly.

- Second solution: create a StrategyParameters class that contains all the parameters. This works as well, but a) it's not clear which parameters are used for which strategies and b) you now have direct coupling between all of the different strategies since their options are amalgated into one (potentially huge) class. Ugghh. There have been some papers discussing a generic, abstract Parameters class and then having arrays of Parameter subclass instances. So you could have an IntParameter subclass, a BoolParameter subclass etc. It might solve this issue, but there is a much bigger problem here.

- Overarching problem of the two previous solutions is that the run method in the trading bot needs to know about implementation details of particular strategies. The decoupling we wanted to achieve with the pattern is now undone again.

- Final solution: make the parameters part of each strategy subclass, and set them in the initializer. Result: a) parameters are at the place where they're used b) they are set when the concrete strategy is created, so you don't introduce extra coupling (it's already coupled there), and c) the run method doesn't need to know anything about specific parameters.

- Conclusion: when you want to use different parameters with the strategy pattern, set them in the initializer. This doesn't introduce extra coupling. It's also the simplest solution in the end. And there's no need for complicated class structures to try to deal with different parameter types. If you can't set the parameter values in the initializer for some reason, you could always add get and set methods to change them. But be careful where you do that, because at that stage, you're introducing coupling. And in that case, you might want to rethink your design because it points to a potential issue.
