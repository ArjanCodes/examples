## Introduction (talking head)

In the last two parts, I showed you the first steps to refactor a data science project. I also made a start in setting up the Runner class that's going to form the basis of how overall code will be setup. Today, I'm going to complete the work.

If you want to become better at taking software decisions, I have a free guide for you that shows you my process in 7 steps. You can get it at arjancodes.com/designguide. It's pretty short, won't cost you much time to read it, but I think you'll find it helpful to improve the way you approach organizing your code and designing your software. So, arjancodes.com/designguide.

# Code recap (screencast)

Very quickly explain the code, and recap what I've done in part 1 and 2.

# Design principles for data science (talking head)

I've talked a lot about software design on this channel, both design principles and design patterns. There's one particularly important design principle to be aware of for data science, and that's the Information Expert Principle. It's part of the GRASP set of principles by Craig Larman. According to this principle, you should assign responsibility to the information expert - the part of the code that has the information necessary to fulfill the responsibility. In other words, the design of the software follows the structure of the data and how it's being used.

As you'll see in a minute, I won't use design patterns all that much. It's more about thinking about how the data is organized and how you can set everything up so that things flow logically without having too much coupling.

## Main changes (screencast)

- The main code for running the epochs has way too many responsibilities, and also contains a lot of duplication. Let's create a Runner class that allows us to run a single iteration over the data.
- I'm also adding a separate run_epoch method to run a single epoch. Notice that the runner.py file is independent of TensorboardExperiment now. Runner is a good example of applying the Information Expert Principle. It has both the data for running an iteration, as well as the methods to run that iteration. It also keeps track of the past batches, instead of having to keep track of that in the main code.
- The main function calls the run_epoch method and is now much simplified.
- Currently, directories and files used in the code are all over the place. Let's move any of those settings to the top. Load_data.py will no longer have directory/file mentions in there. We can create general version of the load_data methods. I'm removing some of the asserts, because these are specific to a particular dataset and do not belong here. You could (and probably should) add separate data validation systems in the future, but that's out of the scope of this video.
- Dataset.py gets a generic create_data_loader function, which also removes some of the code duplication there.
- If you now look at main.py, you'll see that there are no longer any mentions of low-level stuff list ds.load_data. Also, the code is much shorter, and all settings are in a single place. You can now even separate out all the settings and put them in a separate (JSON) file. Now all the analysis code is generic and you can use it for any dataset.

## Final thoughts (talking head)

As you've seen, I haven't really used many design patterns in this refactoring. A lot of the refactoring work concerned splitting code into separate methods or functions, introducing abstractions to reduce coupling (such as cleaning up the ExperimentTracker class), and making sure that configuration settings are in a single place. Let me know in the comments if you have any other suggestions for further improving this code. But the main takeaway is this: in data science projects, the data is central. Design your code around the data, and use the information expert principle to assign responsibilities close to the data that they need.

That's the first way to think about this. The second way is to consider how objects or modules communicate with each other. You generally want to design the system in such a way that the amount of different data that has to flow between them is minimized. In the code example, you see this problem in the first version of dataset.py, where it needs to import lots of specific loading functions. Or in the original main.py file, where the code inside the for-loop depends on lots of variables defined outside of it.

So if two pieces of code are communicating and sending lots of different data to each other, you should probably rethink your design and try to optimize how these pieces of code communicate. It's basically what I tried to do with the Runner class and the run_epoch method.

Another thing that helps you manage more complex code is to use type hints. As you saw type hints are not always properly implemented in the libraries you use, but if you at least try to use them in your own code, it helps avoid some problems like mixing reals and floats.

I hope you enjoyed this closer look at software design for data science projects. Thanks again to Mark Todisco for providing the original example code. I hope you found this helpful - if you did give this video a like and consider subscribing to my channel so you don't miss anything. Thanks for watching, take care and see you next time!
