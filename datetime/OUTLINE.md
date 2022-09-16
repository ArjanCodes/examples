# A deep dive into dates and time in Python

Working with date and time data is one of the most challenging tasks in Data Science as well as programming in general. While dealing with different date formats, different time zones, daylight saving time, and whatnot, it can be difficult of keeping track of what days or times you are referencing.

The reason that programming with dates and times can be such a pain, is due to the fundamental disconnect between the ordered and regular fashion a computer program prefers its events to be, and how irregular and unordered ways in which humans tend to use dates and times.

One great example of such irregularity is daylight time saving, adapted by the United States and Canada. What they essentially do is set the clock forward one hour on the Second Sunday of March, and set back one hour on the First Sunday in November.

However, things might get more complicated if you factor in Time Zones into your projects. Ideally, timezones should follow straight lines along the longitudes, however, due to politics and historical reasons, these lines are seldom straight.

Most of the computers count time from an arbitrary point in time called the Unix epoch: January 1st, 1970, at 00:00:00 hours UTC. I'll talk more about UTC later.

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

The aware objects like datetime, date, and time have an additional optional attribute to them, called the tzinfo. But tzinfo itself is an abstract class. To deal with these, you need to exactly know which methods are needed. Handling timezone problems are eased by the pytz module. Using this module we can deal with daylight savings time in locations that use it and cross-timezone conversions.

Where are these timezones and daylight savings settings coming from, you might wonder? Well, basically, all software in the world retrieves that information from a centralized timezone database. Which is currently maintained by one guy in California. It's a fascinating story, I don't have time to dive into it in this video, but there's a link in the description to an article on Medium that covers this story.

(show timezone examples - `datetime_tz.py`)

# Datetime limitations

The built-in datetime package in Python is nice, but it has some limitations.

First, there are lots of different modules and types: date, time, datetime, calendar, dateutil, tzinfo, timedelta, and more. It gets confusing pretty quickly if you need to do more advanced things with dates and times.

Timezone conversion with datetime is not bad, but you need to create a tzinfo object explicitly to convert a datetime to another timezone.

By default, datetime is timezone-naive: it doesn't take timezones into account unless you explicitly indicate that it should.

Over the past few years a lot of things have been improved like adding support for parsing ISO 8601 strings, but there are still some functionalities that are missing from datetime, in particular humanizing dates and timespans.

So, over the years, people have developed alternatives to datetime, packages such as Arrow, Delorean and Pendulum. These packages generally offer a nicer interface than the standard datetime package. I won't go into detail for each of these packages since they all mostly try to solve the same limitations, but I am going to take a closer look at Pendulum.

Pendulum provides a drop-in replacement for the datetime class, but adds simpler timezone handling, datetimes are timezone-aware by default, and it has a bunch of extra features such as localization, or being able to easily write a human-readable version of a timespan.

Let's take a look at how Pendulum works. But before I do that, I'd really appreciate if you would take the "time" to hit the like button if you're enjoying this video so far. It's going to help YouTube recommend my content to others as well.

# Show pendulum example

See: `pendulum_example.py`

Localization is a topic all in itself. I'd like to cover it in more detail in the future, but I did a miniseries about creating a dashboard application where I also touch on localization. I've put a link to the first part of that series at the top.

# Final thoughts

So, should everyone switch to a library like Pendulum? Well, it's nice, it adds very useful extra features. But, a couple of things to think about:

1. Pendulum hasn't seen a new release for a while. The last version on GitHub was published over two years ago. This is always a risk with using external packages: are they being actively maintained, and for how long?

2. The builtin datetime package is being worked on as well. There are only minor changes in the datetime package in Python 3.11, like a slightly more robust `fromisoformat` method, but as more functionality is added, you might not need an external package anymore. And then you potentially have to do a lot of refactoring work to move away from the external package. Though Pendulum does inherit directly from the datetime class, which reduces the risk somewhat.

3. Do you really need the extra features? If you don't, then simply stick to the builtin datetime module. It's not perfect, but it's pretty good.

Hope that this video and gave you some food for thought about dealing with dates and times. Next to datetime, Python has lots of other interesting packages as well. For example, pathlib is really interesting as well. If you want to learn more, check out this video.

Thanks for watching, take care and see you next week.
