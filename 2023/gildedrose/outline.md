- Today I’m going to take a stab at refactoring the Gilded Rose Kata.
- The Kata was originally created by Terry Hughes.
- If you want to try this yourself, there’s a link to the Git repository with the Kata in different programming languages in the description.
- It’s really fun, but what’s interesting is that this Kata teaches an important lesson about dealing with legacy code.
- You’ll see what I mean later.

## Steps for refactoring Gilded Rose

- Briefly show the Kata description.
- As you know, every respectable inn runs their own custom Python scripts!
- Before I start refactoring anything, let’s analyze the code and get an idea for what’s going on.
- Overall, items have a sell-in time and a quality level. Both of these things are updated every day. There’s a default way to do it, but several items have a different behavior.
- Currently, it’s really hard to work with this code because everything is basically mixed up in a single function. It’s a complete pain if we want to add a new type of item with its own custom behavior.
- The goal of the refactoring is going to be split out the behavior so that we clearly have a default behavior, and there’s an easy way to introduce new item types with custom behaviors.
- Especially when you’re refactoring legacy code, unit tests are your safety net.
  - My approach for refactoring legacy code is to start by writing tests.
  - Then, start with the easiest thing to isolate, work on that first, and then continue to more complex operations.
- Let’s first fix the test that checks if the name stays the same. Then, I’m going to define a number of generic tests, just to cover the cases that are not item-specific.
- Then, let’s write the tests that cover the special cases for each of the item types. Let’s write the tests for aged brie, backstage passes and sulfuras.
- I’m going to start by simplifying the update_items functions by splitting out the for-loop. This reduces indentation one level and makes the code easier to work on. After each refactoring step, I run the tests to make sure everything is still working as intended.
- Next, I’m going to replace all the hardcoded strings by constant values. This is going to make the code a bit easier to read, and it’s also going to ensure that when I make changes, I won’t accidentally make a typo.
- As you can see, until now I’ve done nothing else than just minor tweaks and spent most of my time writing tests. Proper preparation is half of the job!
- Currently, changing the sell-in days number is in the middle of the code that changes the quality. I’d like to move it to the top of the code so we can split it out later. Looking through the code, that’s going to affect the else part of the first if-statement (dealing with the various sell-in day cases). It’s an easy fix to shift the numbers by 1 though, so I’m moving the sell-on days change to the top of the function and then change the numbers 11 and 6 to 10 and 5 respectively. Run the tests to make sure this doesn’t break anything.
- Next, let’s start simplifying the logic. Currently, there a lot of “≠” comparisons that make it hard to understand what code is executed for which item type. But, you can step-by-step reverse the logic to ultimately create an if-statement that simply looks at each of the different cases and then applies the necessary logic.
- Now that we have an if-statement that covers the case for each different item type, the next step is to refactor the code so that it’s easier to add new item types. In order to do that, I’m going to create a simple class hierarchy (based on a Protocol class) that models the different types of behavior for the different items. I’ll start by creating a default updater that contains the default behavior. Then, I’ll create item-specific subclasses that can override some of the default behavior and replace it with something else. I use a dictionary to map the item types to custom behavior so we can add more custom behavior easily later by just extending the dictionary. Run the tests again after making each change.
- Now we can introduce a new conjured type. Let’s first add the test for this and make sure that it fails (red-green-refactor!)
- Then, implement the ConjuredUpdater class and add it to the dictionary. The test should now pass.

## Final thoughts

- It was really fun working on this code refactoring!
- How did I do? What would you do differently? Let me know in the comments!
- Major takeaways for me were:
  - Never start refactoring without a plan! Analyze the code first. Define what your end goal is (depends on why you need to touch the code). Write down what roughly the steps are going to be to get to your end goal.
  - Common things you might do to improve and simplify legacy code are reversing logic, changing the order of things, or splitting more or less isolated parts of the code into separate functions
  - Start with relatively simple changes. Sometimes you might even make a change that you later throw away again as it was purely an intermediate step. Even small things like putting a string value into a constant can be a lifesaver!
  - And finally: tests are your safety net. I initially was thinking about already changing a few things without test writing, but that felt very uncomfortable! Especially when working on legacy code: write the tests first and then refactor step-by-step.
- If you enjoyed this refactoring video, and you learned something from it, you might also like my Code Roast video series, where I work on a piece of code submitted by my audience. Thanks for watching, take care!

# Links

- https://github.com/emilybache/GildedRose-Refactoring-Kata
