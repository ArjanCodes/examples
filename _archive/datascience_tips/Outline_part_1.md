## Introduction (talking head)

This video is a refactor of a data science project kindly provided by Mark Todisco. The project is a basic hand-written digit recognition model based on a well-known dataset called MNIST (see the link in the description of the video).

This is a three-part video. In first part, I'm mainly going to look at a few design issues in the code. I'm also going to cover a really nice functional mechanism for dealing with data in a pipeline. And then in the second and third parts, I'll dive more into how data flows in the application and how we can improve that by designing things differently.

Disclaimer: I'm not a data scientist, I'm purely approaching the code from a software design point of view. So it's possible that I'm going to do some things that you don't think make a lot of sense. I still hope though that you find some use in how I refactor the code, let me know in the comments what you think and if I should do more of these data sciency kinds of videos in the future.

Before we start though, I have something for you. It's a free guide to help you make better software design decisions in 7 steps. You can get it at arjancodes.com/designguide. I've tried to keep the guide short and to the point, so you can get the information quickly and apply it immediately to what you're doing. So, arjancodes.com/designguide. That link is also in the description of the video.

But let's first look at the code!

## Example explanation (screencast)

Explain the code used as a basis for the refactoring

## A few general remarks (talking head)

Python is a very popular language for data science. Most Data Science studies focus on the theory of data science, statistics and machine learning, and along the way you learn to use Python as well as a collection of tools such as Pandas and Tensorflow. In many cases, this is all you need to know.

Unfortunately, most studies don't really pay any attention to how to setup a more complicated data science project, and how to make sure that the code you write makes sense, that it's easy to change, and that you can reuse it in the future. That's where software design comes in.

## Main changes (screencast)

- ExperimentTracker is an abstract class, but kind of a mess. It has partial implementation (like storing the stage). At the same time, it's not very useful, because for example in the main code, we call `set_stage` which is not part of the abstract class. So that means at the moment, the abstract class doesn't provide any abstraction. Let's fix that by turning it into a Protocol class, remove any implementation from it, and add the set_stage method. Now TensorboardExperiment can implement those methods.
- Change Real -> float. Sometimes, Real is used, sometimes float, which is inconsistent and you notice this as soon as you start to add type hints. I'll use float everywhere for consistency.
- Metric can be simplified to become a dataclass.
- Stage should be an enum instead of a frozen dataclass since it behaves more like an enum.
- For the model (LinearNet), we can simplify things by using function composition instead of storing the value over and over again in the same variable. In PyTorch, you can actually use a network for this.

## About composing functions (talking head)

When you're working with data, it often happens that you need to create some sort of pipeline for processing data. For example, delete partial entries or outliers, normalize the data, transform the data into another format, and then export it to a file or store it in a database. It's useful to have a definition of what the pipeline is and let that be an object or module of some sort, so you can push various collections of data through the same pipeline. PyTorch supports this by defining a network. But you may not always want to use PyTorch. So what to do in that case?

One way to do it is to call a sequence of functions, store each intermediate result in a variable and pass that variable to the next function. If you have many of those functions, it becomes annoying to declare a variable for each intermediate result, so, it seems reasonable to reuse the variable for this, like in the example code. However, this is not ideal. Reusing a variable means that it's no longer clear what the variable actually means, because it means different things depending on where you are in the pipeline. If you transform data, you won't be able to use typing for your variable, because that changes over time.

A much cleaner way to do it is by using function composition. Let's see how that works.

## Composing functions example (screencast, compose_example.py)

Show that you can compose functions. The basic way to do it is simply chain the functions. But that leads to unreadable code as you add more functions to the sequence. Second option is to create a helper 'compose' function that gets the functions to be called as arguments.

IF you're using Scikit Learn, it has a concept similar to what PyTorch offers, which is called a Pipeline. This also allows you to compose functions and call them on a some input date. There's a link in the description with more information.

https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html

This is the end of part one. Next week, I'm going to finish this refactoring. We're going to take a closer look at how data is handled by the code and how we can use design principles to improve that.
