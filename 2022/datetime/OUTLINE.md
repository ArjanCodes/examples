# A deep dive into dates and time in Python

Working with date and time data can be really challenging. With all the different date and time formats, ISO standards, different time zones, daylight saving, adjusting for time travelling with tachyon particles, it goes on and on.

Today, I want to take you through how Python's builtin datetime package works, talk about some of the alternatives out there to help make dealing with dates and times easier, and whether those alternatives are actually necessary.

Learning about these things helps you become a better software engineer, and hone your critical thinking skills. If you want to take this a step further, I have a free workshop for you that teaches you how to diagnose existing code and quickly see what the main problems are. It's one of the most important things to get good at, especially as you start moving into a more senior position. You can get access to the workshop by going to arjan.codes/diagnosis. The workshop is organized around three factors and contains loads of code examples, also from well-known Python packages. Just grab it for free at Arjan.codes/diagnosis, the link is also in the description.

Why is dealing with dates and times such a pain? It's a dichotomy between on the one hand computer software which tends to ordered and structured and generic and on the other hand the quite unstructured way we deal with dates and times. Things are never the same. Some years don't have the same number of days because they're a leap year. Months don't have the same number of days. Each day doesn't have the same number of hours if you consider daylight time saving. Not all countries have daylight time saving, and those that do may apply daylight time saving at a different moment. Then we have time zones which are not divided by longitudal geodesics due to political and historical reasons. In short, it's a mess.

In our little computer bubble we do have some kind of standard way of representing dates and time. Most computer system count time starting from an arbitrary point in time called the Unix epoch: January 1st, 1970, at 00:00:00 hours UTC. What's UTC? I'll talk more about that in a minute.

# Unix time (screencast)

So, Unix time is measured in seconds from January 1st, 1970. You can easily view the current Unix time with a few lines of Python code.

```python
import time
print(time.time())
```

# The year 2038 problem (screencast)

Here is an interesting fact about Unix time. Since most of the older operating systems are 32-bit, they store the Unix time in a 32-bit signed integer.

You already know where this is going if you are familiar with the Y2K Problem. Storing in a 32-bit signed integer format means at 03:14:07 on January 19th, 2038, the integer will overflow, resulting in what’s known as the Year 2038 Problem. Python itself won't have an issue with this because integers in Python are not represented by a fixed number of bits. But of course Python relies on lower level OS functions to retrieve the time.

So if you want to avoid catastrophic consequences to your critical systems in 2038, make sure that you update them to use a 64-bit OS somewhere within the next 15 years. If you're planning to still run a critical system on a 32-bit OS in 2038 though, can you please fire yourself? The world thanks you.

# UTC

As I mentioned earlier, Unix time is expressed in the UTC timezone. UTC stands for Universal Time Coordinated (UTC), or Coordinated Universal Time. Before 1972, this time was called Greenwich Mean Time (GMT), sometimes erroneously called Greenwich Meridian Time. And it's pronounced "grenitsch", not "green witch" - unless you live in the land of Oz.

UTC is a coordinated time scale, maintained by the Bureau International des Poids et Mesures (BIPM). It's not adjusted for daylight saving time so there's always twenty-four hours in a day. It is also known as "Z time" or "Zulu Time". Which sounds way cooler than UTC. Let's take a look at how we deal with dates and times in Python.

# Using dates and time in Python (screencast)

Show basic usage of dates and time in Python (`datetime_basic.py`).

# How to deal with Timezones

Date and Time objects can be broadly divided into two categories, mainly ‘Aware‘ and ‘Naive‘. In simple words, if an object contains the timezone information it is Aware, or else, Naive.

In Python, objects like datetime have an optional property tzinfo that contains the time zone information. By default datetime is timezone naive, so this object isn't set to anything. If you want timezone-aware datetimes, you need a module that can deal with all the issues related to timezones that I mentioned earlier. In Python, we have the pytz package for this. It's not built into python, you have to add it as a dependency.

You might wonder where all these timezone and daylight savings settings come from. Basically, most software in the world retrieves that information from a centralized timezone database. Which is currently maintained by one guy in California (well, kinda). It's a fascinating story, I don't have time to dive into it in this video, but there's a link in the description to an article on Medium if you want to read more about it.

Now let's take a look at some examples of how to deal with timezones in Python.

(show timezone examples - `datetime_tz.py`)

# Datetime limitations

The built-in datetime package in Python is nice, but it has some limitations.

First, there are lots of different modules and types: date, time, datetime, calendar, dateutil, tzinfo, timedelta, and more. It gets confusing pretty quickly if you need to do more advanced things with dates and times.

Timezone conversion with datetime is not bad, but you need to create a tzinfo object explicitly to convert a datetime to another timezone.

By default, datetime is timezone-naive: it doesn't take timezones into account unless you explicitly indicate that it should.

Now, over the past few years a lot of things have been improved in the datetime package like adding support for parsing ISO 8601 strings, but there are still some functionalities missing, such as humanizing dates and durations.

People have developed alternative packages that deal with dates and times such as Arrow, Delorean and Pendulum. These packages generally offer a nicer interface than the standard datetime package. I won't go into detail for each of these packages since they all mostly try to solve the same limitations, but I am going to take a closer look at Pendulum today.

Pendulum provides a drop-in replacement for the datetime class, but adds simpler timezone handling, datetimes are timezone-aware by default, and it has a bunch of extra features such as localization, or being able to easily write a human-readable version of a timespan.

Let's take a look at how Pendulum works. But before I do that, I'd really appreciate if you would take the "time" to hit the like button if you're enjoying this video so far. It's going to help YouTube recommend my content to others.

# Show pendulum example

See: `pendulum_example.py`

Localization is a topic all in itself. I'd like to cover it in more detail in the future, but I did a miniseries about creating a dashboard application where I also touch on localization. I've put a link to the first part of that series at the top.

# Final thoughts

So, should everyone switch to a package like Pendulum? Well, it's nice, it adds very useful extra features. But, here are a couple of things to think about:

1. Pendulum hasn't seen a new release for a while. The last version on GitHub was published over two years ago. This is always a risk with using external packages in production code, you have to consider whether they're being actively maintained, and for how long?

2. The builtin datetime package is being worked on as well. There are only minor changes in that package in Python 3.11, like a slightly more robust `fromisoformat` method, but as more functionality is added, you might not need an external package anymore. And then you potentially have to do a lot of refactoring work to move away from the external package. Though Pendulum does inherit directly from the datetime class, which reduces that risk somewhat.

3. Do you really need the extra features? If you don't, then simply stick to the builtin datetime pakcage. It's not perfect, but it's pretty good.

Hope that this video gave you some food for thought about dealing with dates and times in your own code. Next to datetime, Python has lots of other interesting packages as well. For example, pathlib. If you want to learn more about dealing with paths, check out this video.

Thanks for watching, take care and see you next week.
