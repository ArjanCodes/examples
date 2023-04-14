## Introduction (talking head)

Last week, I showed you the first steps to refactoring a data science project. In this part, I'm going create a Runner class that will be responsible for running the main training and testing loop, which is currently still in the main.py file.

If you want to learn more about data science, Skillshare, who's the sponsor of this video, is a great place to start.

# Code recap (screencast)

Very quickly explain the code, and recap what I've done in part 1.

# Design principles for data science (talking head)

I've talked a lot about software design on this channel, both design principles and design patterns. There's one particularly important design principle to be aware of for data science, and that's the Information Expert Principle. It's part of the GRASP set of principles by Craig Larman. According to this principle, you should assign responsibility to the information expert - the part of the code that has the information necessary to fulfill the responsibility. In other words, the design of the software follows the structure of the data and how it's being used.

As you'll see in a minute, I won't use design patterns all that much. It's more about thinking about how the data is organized and how you can set everything up so that things flow logically without having too much coupling.

## Main changes (screencast)

- The main code for running the epochs has way too many responsibilities, and also contains a lot of duplication. Let's create a Runner class that allows us to run a single iteration over the data.
- I'm also adding a separate run_epoch method to run a single epoch. Notice that the runner.py file is independent of TensorboardExperiment now. Runner is a good example of applying the Information Expert Principle. It has both the data for running an iteration, as well as the methods to run that iteration. It also keeps track of the past batches, instead of having to keep track of that in the main code.
- The main function calls the run_epoch method and is now much simplified.

## Talking head

Next week, I'm going to complete this project. I'll be using the code from this week's video as a starting point.
