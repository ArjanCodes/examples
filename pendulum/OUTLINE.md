# Pendulum

In this video I want to cover dealing with dates and time. I'll be using the Pendulum library.

Working with date and time data is one of the most challenging tasks in Data Science as well as programming in general. While dealing with different date formats, different time zones, daylight saving time, and whatnot, it can be difficult of keeping track of what days or times you are referencing.

The reason that programming with dates and times can be such a pain, is due to the fundamental disconnect between the ordered and regular fashion a computer program prefers its events to be, and how irregular and unordered ways in which humans tend to use dates and times.

One great example of such irregularity is daylight time saving, adapted by the United States and Canada. What they essentially do is set the clock forward one hour on the Second Sunday of March, and set back one hour on the First Sunday in November.

However, things might get more complicated if you factor in Time Zones into your projects. Ideally, timezones should follow straight lines along the longitudes, however, due to politics and historical reasons, these lines are seldom straight.

Most of the computers count time from an arbitrary point in time called the Unix epoch: January 1st, 1970, at 00:00:00 hours UTC. Before 1972, this time was called Greenwich Mean Time (GMT).

but is now referred to as Coordinated Universal Time or Universal Time Coordinated (UTC). It is a coordinated time scale, maintained by the Bureau International des Poids et Mesures (BIPM). It's not adjusted for daylight saving time so there's always twenty-four hours in a day. It is also known as "Z time" or "Zulu Time". Which sounds way cooler than UTC. Are you still with me?

Unix time is measured in seconds from January 1, 1970. You can easily view the current Unix time with a few lines of code in Python.

# The year 2038 problem

Here is an interesting fact about Unix time. Since most of the older operating systems are 32-bit, they store the Unix time in a 32-bit signed integer.

You already know where this is going if you are familiar with the Y2K Problem. Storing in a 32-bit signed integer format means at 03:14:07 on January 19th, 2038, the integer will overflow, resulting in what’s known as the Year 2038 Problem. Python itself won't have an issue with this because integers in Python are not represented by a fixed number of bits. But of course Python relies on lower level OS functions to retrieve the time.

So if you want to avoid catastrophic consequences to your critical systems in 2038, make sure that you update them to use a 64-bit OS somewhere within the next 15 years. If you're planning to still run a critical system on a 32-bit OS in 2038 though, can you please fire yourself? The world thanks you.

# Using dates and time in Python

Show basic usage of dates and time in Python.

# How to deal with Timezones

Date and Time objects can be broadly divided into two categories, mainly ‘Aware‘ and ‘Naive‘. In simple words, if an object contains the timezone information it is Aware, or else, Naive.

The aware objects like datetime, date, and time have an additional optional attribute to them, called the tzinfo. But tzinfo itself is an abstract class. To deal with these, you need to exactly know which methods are needed. Handling timezone problems are eased by the pytz module. Using this module we can deal with daylight savings time in locations that use it and cross-timezone conversions.

Where are these timezones and daylight savings settings stored, you might wonder? Well, basically, all software in the world retrieves that information from a centralized timezone database. Which is currently maintained by one guy in California. It's a fascinating story, I don't have time to dive into it in this video, but there's a link in the description to an article on Medium that covers this story.

(show timezone examples)
