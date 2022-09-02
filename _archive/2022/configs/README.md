# Video introduction

Most Data Science code, whether you're processing or analysing data, doing machine learning or web scraping, you're going to have a bunch of configuration settings. But where's the best place to define these settings? How do you design your code so that your settings are easy to find, and easy to change? I'm going to give you a few tips in this video, and also talk about a really useful package to help you with this.

# Explain the example

- Mainly focus on the configuration settings.
- Also briefly show before version.

# The problem

So what makes dealing with configuration settings so hard? First, you'll need them in lots of different places in your code. Your data model might need paths to training and testing data, you experiment tracking service needs to know where to put experiment logs, your data processing system needs to know what the settings are of each step in the pipeline, your neural network might have a bunch of settings and algorithm parameter. Second, you also want a single, logical place where you can easily keep track of these settings.

This seems to lead to an unsolvable problem. If you store all configuration settings in a single place then you either have to pass them around everywhere, leading to functions with lots of arguments, each passing through a bunch of settings to the lower level function, leading to weak cohesion. On the other hand, if you instead turn these settings into global variables, then you suddenly have a lot of coupling to the global namespace.

In the example, I basically went for the solution of storing all config settings in a single place. For this code, it worked fine, because it's not that complicated, but for more complex projects you don't want your main file to be filled with a bunch of configuration settings.

So what are a few other solutions?

1. You could define each of the settings locally near the place where they're being used. That way, it's clear what setting is used where, and it provides a kind of structure. But then your variables will be in various places in your code, which is also not ideal.

2. You could use environment variables. This is a nice solution. You define environment variables outside of your code and then use them whenever you need them. You can the run your script using different settings without having to change the code. Python-dotenv is a nice library that you can use to store the values of these variables in a .env file and then load them in as environment variables. This avoids the problem of defining all settings in a code file and having to pass them around. But, there is no structure whatsoever to these variables, and you'll end up with lots of references to environment variables in your code. It becomes hard to understand then which variable is what and where it is used.

3. Instead of using a .env file, you can also read the settings from a JSON or a YAML file. This has the additional advantage that it can provide some structure to your settings. If you organize your settings in object and sub-objects, you can then load all the data in your main file, and pass the subobjects around, instead of the specific settings. That way, you can match the structure of the object to the layer of the application you're in. For example, you might have an object 'experiment tracker settings' containing a group of settings for the experiment tracking service. You can then pass this object as a whole to the experiment tracker, which then extracts the specific settings from it.

There's a really nice library called Hydra that takes this idea to the next level. With Hydra you can create complex hierarchies of setting files, determine which config file to use when you run your script, or even run your script a number of times with different settings. Let's see how it works.

# Explain Hydra example

- Basic configuration using data classes
- Default values
- Notice Hydra main typing issue

# Final thoughts

With all that out of the way, here's my advice for properly dealing with configuration settings:

1. Define your settings in a single place, outside of the code, preferably in a JSON/YAML file, and load them in your main file.
2. Provide structure to your configuration settings, so that you don't have to pass too many specific settings around but can use objects instead.
3. Use a package like Hydra to make dealing with confuguration settings easier.

I hope you enjoyed this video. If you did, give this video a like, and consider subscribing if you're enjoying my content. If you want to watch me refactor a complete data science project, watch this video next. Thanks for watching, take care and see you soon.
