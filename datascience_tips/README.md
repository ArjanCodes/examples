## Video outline (talking head)

This video is a refactor of a data science project kindly provided by Mark Todisco. The project is a basic hand-written digit recognition model based on a well-known dataset called MNIST (see the link in the description of the video). Let's first look at the code!

## Example explanation (screencast)

Explain the code used as a basis for the refactoring

## A few general remarks (talking head)

Python is a very popular language for data science. Most Data Science studies focus on the theory of data science, statistics and machine learning, and along the way you learn to use Python as well as a collection of tools such as Pandas and Tensorflow. In many cases, this is all you need to know.

Unfortunately, most studies don't really pay any attention to how to setup a more complicated data science project, and how to make sure that the code you write makes sense, that it's easy to change, and that you can reuse it in the future. That's where software design comes in.

I've talked a lot about software design on this channel, both design principles and design patterns. There's one particularly important design principle to be aware of for data science, and that's the Information Expert Principle. It's part of the GRASP set of principles by Craig Larman. According to this principle, you should assign responsibility to the information expert - the part of the code that has the information necessary to fulfill the responsibility. In other words, the design of the software follows the structure of the data and how it's being used.

As you'll see in a minute, when I refactor the code you just saw, I won't use design patterns all that much. It's more about thinking about how the data is organized and how you can set everything up so that things flow logically without having too much coupling.

## Main changes (screencast)

- ExperimentTracker is an abstract class, but kind of a mess. It has partial implementation (like storing the stage). At the same time, it's not very useful, because for example in the main code, we call set_stage which is not part of the abstract class. So that means at the moment, the abstract class doesn't provide any abstraction. Let's fix that by turning it into a Protocol class, remove any implementation from it, and add the set_stage method. Now TensorboardExperiment can implement those methods.
- Change Real -> float. Sometimes, Real is used, sometimes float, which is inconsistent and you notice this as soon as you start to add type hints. I'll use float everywhere for consistency.
- Metric can be simplified to become a dataclass.
- Stage should be an enum instead of a frozen dataclass since it behaves more like an enum.
- For the model (LinearNet), we can simplify things by using function composition instead of storing the value over and over again in the same variable. I'm adding a compose helper function and then use that to compose all the functions. Ideally, I'd like to simply store these functions in a list, but for some reason that doesn't work. Apparently these functions that torch are not pure functions.
- The main code for running the epochs has way too many responsibilities, and also contains a lot of duplication. Let's create a Runner class that allows us to run a single iteration over the data.
- I'm also adding a separate run_epoch method to run a single epoch. Notice that the runner.py file is independent of TensorboardExperiment now. Runner is a good example of applying the Information Expert Principle. It has both the data for running an iteration, as well as the methods to run that iteration. It also keeps track of the past batches, instead of having to keep track of that in the main code.
- The main function calls the run_epoch method and is now much simplified.
- Currently, directories and files used in the code are all over the place. Let's move any of those settings to the top. Load_data.py will no longer have directory/file mentions in there. We can create general version of the load_data methods. I'm removing some of the asserts, because these are specific to a particular dataset and do not belong here. You could (and probably should) add separate data validation systems in the future, but that's out of the scope of this video.
- Dataset.py gets a generic create_data_loader function, which also removes some of the code duplication there.
- If you now look at main.py, you'll see that there are no longer any mentions of low-level stuff list ds.load_data. Also, the code is much shorter, and all settings are in a single place. You can now even separate out all the settings and put them in a separate (JSON) file. Now all the analysis code is generic and you can use it for any dataset.

## Final thoughts (talking head)

As you've seen, I haven't really used many design patterns in this refactoring. A lot of the refactoring work concerned splitting code into separate methods or functions, introducing abstractions to reduce coupling (such as cleaning up the ExperimentTracker class), and making sure that configuration settings are in a single place. Let me know in the comments if you have any other suggestions for further improving this code. But the main takeaway is this: in data science projects, the data is central. Design your code around the data, and use the information expert principle to assign responsibilities close to the data that they need.
