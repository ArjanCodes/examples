# The Ultimate Guide To F-strings

In this video, I'm going to cover f-strings. I'm quite sure that at least one of the features I show you in this video is going to be new to you.

F-strings have been introduced to Python in version 3.6. They allow you to do string interpolation, as an alternative to string formatting using the percentage operator, or the str.format method.

## Number formatting

## Padding and alignment

## Repr vs Str

The difference between str() and repr() is: The str() function returns a user-friendly description of an object. The repr() method returns a developer-friendly string representation of an object.

In f-strings, the **str** function is used by default to construct a string of an object, but if you use the !r extension it calls the **repr** function instead.

## Date and time formatting

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

I hope you enjoyed this video. If you did, give it a like and consider subscribing to my channel. Thanks for watching, take care, and see you soon.
