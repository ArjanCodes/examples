## About this video

The code smells video from a couple of weeks ago did really well, so I've decided to do another one!

## Video outline

- What are code smells?

  - The term code smell comes from Martin Fowler's book on refactoring.
  - A code smell is not a bug, but a hint that something's wrong in your code.
  - Often points to a deeper problem/design flaw
  - Pragmatic approach to code smells is that you should consider these on a case-by-case basis. Use them to point out design issues in your code and fix them if possible.
  - Purist approach: all code smell are actually code stenches and shouldn't be allowed at all.

- Let's look at a particularly smelly example and make it smell all rosy again!

- Code smell #1: abusing types for something else

  - We're using a str type to distinguish between roles. But str can basically be anything, "slacker", "troublemaker", etc. We don't want those kinds of roles in our company, now do we?
  - FIX: Move to enum to fix the problem

- Code smell #2: duplicate code

  - The find_xxx methods basically all do the same thing, except for a different role.
  - FIX: Refactor into one method that accepts the role as a parameter

- Code smell #3: not using available built-in functions

  - Python has lots of built-in methods to make your life easier, especially for lists. List comprehensions in particular are a really powerful, and there are other alternatives that are suitable as well - think of functions like map or filter. Use them!
  - Find_employees methods use a loop, but there are easier ways to do this
  - FIX: use a list comprehension to reduce the find_employees function to a single line

- Code smell #4: vague identifiers (amount in HourlyEmployee -> hours_worked)

  - HourlyEmployee has an 'amount' variable that stands for the nr of hours worked.
  - This is a very vague name that doesn't explain at all what the variable means and what the unit is.
  - FIX: Change it to hours_worked

- Code smell #5: using isinstance to separate behavior

  - pay_employee needs to do different things depending on the type of employee
  - this approach leads to a lot of coupling since we need to update this method for every new employee type, with big if-else statements as a result
  - FIX: add a pay() method to Employee, use inheritance for subclass-specific implementations

- Code smell #6: using boolean flags to make a method do 2 different things

  - take_a_holiday method does two different things depending on a boolean flag (either let someone take a holiday, or pay out the holiday to the employee)
  - This leads to low cohesion (one method having too many responsibilities), and methods that are harder to understand what they do
  - FIX: split the method in two

- Code smell #7: empty catch/except clause

  - payout_a_holiday has a try with an empty except.
  - This is bad, because exceptions are now ignored completely, and can't be handled outside of the method call anymore. Even worse: these kinds of catch-all blocks can even ignore SyntaxError or KeyboardInterrupt exceptions in some cases. So your code could have a typo, and you wouldn't know about it.
  - FIX: if you can't do anything with an exception, don't catch it and ignore it, another part of your program might be able to deal with it

- Code smell #8 (bonus): use custom exceptions
  - If you raise a ValueError, this introduces coupling, because the calling code needs to know that if the function raises a ValueError, this can be both an internal Python error, or because of a shortage of holidays. Also, there is no easily accessible information about the context of the errors (remaining vacation days etc).
  - FIX: create a custom VacationDayShortageError that has attributes containing useful error data, such as the remaining available vacation days.
