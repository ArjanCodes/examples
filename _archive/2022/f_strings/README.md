# The Ultimate Guide To F-strings

F-strings in Python are incredibly powerful. And knowing how to use them and their formatting capabilities is going to make a huge difference in how easily you can create logging messages, or display information in a way that's easy to read. So that's why I'm diving into f-strings in this video and show you what you can do with them. And I'm quite sure that there's going to be something in this video that you didn't know about f-strings.

You might use formatted strings already in your code, for example as part of your logging system to detect problems and fix bugs. In general, the skill of being able to quickly identify problems in your code is really important. If you want to learn how to do this, you should check out my free Code Diagnosis workshop where I teach you the most important things to look for when you want to quickly identify design problems in your code. It's based on my own experience reviewing code trying to do that efficiently while still finding the problems fast. You can sign up for the workshop at arjan.codes/diagnosis. It contains a ton of useful advice and practical code examples that you can apply right away to train your diagnosis skills. So, arjan.codes/diagnosis, the link is also in the description.

F-strings have been introduced to Python in version 3.6. They allow you to do string interpolation, as an alternative to string formatting using the percentage operator, or the str.format method.

## Number formatting

## Padding and alignment

## Repr vs Str

The difference between str() and repr() is: The str() function returns a user-friendly description of an object. The repr() method returns a developer-friendly string representation of an object. If you're using dataclasses, the repr dunder method is generated automatically for you. If you want to learn more about dataclasses, click the link in the top to watch a video that shows you everything you need to know.

In f-strings, the **str** dunder method is used by default to construct a string representation of an object, but if you use the !r extension it calls the **repr** dunder method instead.

## Date and time formatting

Full list of date and time formatting codes: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes.

If you need better datetime formatting, there's a library called Pendulum: https://pendulum.eustace.io. If you want me to do a separate video about this, let me know in the comments!

## Debugging

## Multiline strings & comments

## F-strings performance

F-strings are faster than the traditional methods of string interpolation. They're even faster than using a prepared template (see speed.py)

## Conclusion - What are the advantages of Python f-strings?

To conclude, the main advantages of using Python f-strings are:

- It is the fastest string formatting method in Python.
- It is more readable.
- It is concise.

In my opinion, there's no reason to still use the other formatting options. F-strings should cover all your formatting needs.

I hope you enjoyed this video. If you did, give it a like and consider subscribing to my channel. Next to string formatting Python has lots of other interesting features, like support for functional programming which is really cool. If you want to learn more, check out this video. Thanks for watching, take care, and see you soon.
