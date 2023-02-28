Hey there, in this video I'm going to take a deep dive into Python's logging package. Now, if you're like me you probably think that logging is kind of boring and not really that important. But trust me, once you see all the things that the logging package can do for you, you'll change your mind. So sit back, relax and let me show you why Python's logging package is so awesome.

# **Why logging instead of just printing?**

- Logging is slightly more complicated to set up and use than print(), but a specific logging solution has several advantages:
- More control over the format of log messages
- More control over how detailed logs should be and being able to dynamically switch between detail levels depending on the need.
- Better management and organization of logs, especially in larger applications.
- You can send logs to different locations, not just the console.

Now that you know why it's useful to use a logging solution instead of just printing stuff, let's take a look at some of the features of Python's logging module.

# **Basic logging classes**

There are several different classes that you need to know about when logging. **Loggers** create the log records. **Handlers** send the records to the right place. Filters determine which records to output. And **Formatters** control how the records look when they are output.

## **Configuring logging**

- By default, there are five levels of severity that you can use to indicate how important an event is. You can use a corresponding method for each level to log events. The defined levels, in order from least severe to most severe, are as follows:
  - DEBUG
  - INFO
  - WARNING
  - ERROR
  - CRITICAL
- The basicConfig() method lets you configure logging. Some of the parameters used most often for basicConfig() are:
- level: Sets the root logger to this severity level.
- filename: Names the file.
- filemode: If you specify a filename, opens the file in this mode. The default is append mode (a).
- format: This is the format of log messages .
- You can use the level parameter to choose how much logging you want. This can be done by passing one of the constants available in the class. This will enable all logging calls at or above that level to be logged.
- Show basic logging example (`logging_to_console.py`)
- Show logging formatting example (`logging_formatting.py`)
- Show example of logging to file (`logging_to_file.py`)

## Integration with logging services

- If you want to have more control over your logging, you can use a logging service.
- Logging services offer easiers ways to visualize and search logs, backup and export logs, structure logs better and make them more easily available to others in your team.
- It's really easy to integrate Python's logging with such a service.
- I'll show you how to do it with Papertrail (btw, this is not a sponsored video - I used them in the past and thought it would serve as a good example)
- Show Papertrail interface and `logging_papertrail.py`.

# **Logging design choices**

- There are several ways in which you can incorporate logging into the application. When you need to log something, you can simply import the logging package and then directly call `logging.info(...)`.
- You can also create a logger object with specific settings for that particular type of logging. This is even needed if you use a platform like Papertrail because you need to define a custom logging handler in that case.
- But then: how do you supply the logging object to the places in your code where you need to log things?
  - Pass it as an argument to every function call or object that uses logging (not ideal because it adds extra arguments everywhere.
  - Create a logger object in another file and then import the object from that file
- Unfortunately, there’s no perfect solution. Probably importing the logger is the least “bad” solution, since you can then - if you want - replace the logger object by something else, as long as it implements the same interface.
