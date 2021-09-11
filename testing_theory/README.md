## Video outline

This video is going to cover the basics of what software testing is.

## What is software testing?

Software testing is the process of verifying that a software system is working as expected. It gives insight into the quality of the software, if testing is done properly. It also provides an objective view on your software that developers can rely on to make decisions about how to improve the software.

There are many different types of tests. I'll cover the most common ones in this video. But before that, let's talk about what tests are not.

## What tests aren't

Tests are not a guarantee that your program is correct. Edsger Dijkstra once said: "Program testing can be used to show the presence of bugs, but never to show their absence.". Let's look at an example that illustrates this.

## Simple testing example (screencast)

All tests pass in this case (note, I'm not using any testing framework here, just asserting that the output is correct). The `add_three_alt` function also passes all tests, but it is clearly wrong. Now suppose you added millions and millions of tests, one for each possible number. Wouldn't that prove that the function is wrong? Nope, because I could add just as many if-statements as I wanted. Even if you added an infinite number of tests, it still wouldn't be a proof, because the function could have side-effects. For example, what if the function used a random number generator to once in a while return a value that is not what it should return? Or use the system time to return a different result, but only on June 8 which happens to be my birthday! So in short, tests will never be a guarantee that your code is correct.

## About proving code correctness

But what if you do want to prove that a piece of code is correct? Actually that's possible using Hoare logic (invented by the British computer scientist Tony Hoare). The central part of Hoare logic is the Hoare triple. This describes how the execution of a piece of code changes the state of the computation. A Hoare triple is of the form {P}C{Q}, where P is a precondition, C is a computation, and Q is a postcondition. In short this means: when the precondition is met, executing the command establishes the postcondition. There are Hoare logic rules for all of the commands defined in structured programming languages, including sequences of commands, loops, and conditionals. So in principle you could use Hoare logic to prove that your code is correct. But of course, as soon as your code grows complex, it quickly becomes impractical to prove correctness.

So what do we do? We use software testing instead to help us get a grasp on at least part of how our code works.

## Different approaches to software testing

When we talk about software testing, often people immediately think about unit testing. Unit testing, and any other testing approach where you run your code with a collection of pre-defined test cases is called dynamic testing. Another approach is static testing, which doesn't require writing test cases, but involves things like code reviews, and even syntax and type checking by your IDE. Passive testing is yet another approach where you don't even look at the software, but at what the software produces such as system logs or analysis of the structure of the database over time to identify anomalies. For example, suppose that you develop an application for schools that stores students and education programs. You could do database checks every once in a while to verify that each student belongs to a valid education program.

## Box testing (Screencast)

Another way to look at testing is to differentiate between white box and black box testing. White box testing looks at the inner structure of the software. Unit tests are a good example of white box testing. But other techniques also exist such as mutation testing, which slightly modifies the source code of a program to see whether the tests pick it up.

Here's an example of running a (manual) mutation test. I'm going to replace the + operator with a - operator in the `add_three` function and verify that all tests fail. This is called a mutant. And we see that the tests all fail. But if we replace the \* in multiply_by_two with a + sign our only test still passes.

(talking head) Black box testing doesn't know anything about the internal working of the code - it looks at what the software does, not how it does it. An example of this is a technique called snapshot testing. Snapshot testing is a technique where you take a snapshot of the state of the system before and after a command is executed. Then you can compare the two snapshots to see if the state of the system has changed. If you build web applications, you can use snapshot testing to compare the HTML and CSS that an app produces and make sure things work as expected. This is for example what React's Jest testing library does.

## Property/invariant testing

Another important concept in determining program correctness is the invariant. An invariant is a logical assertion that is always held to be true during a certain phase of execution. For example, a loop invariant is a condition that is true at the beginning and the end of every execution of a loop. Based on this idea, you could define a certain property that you want to be certain is always true, and then you can test whether this is the case using lots of automatically generated inputs. This is called property-based testing. Let's look at an example.

## Property-based testing example (screencast)

- The `add_three` function could have the property that whatever you put into it, the output is always the input + 3.
- You could also write a test that verifies that applying add_three and then remove_three gives the original input (this is also called Bilbo testing, or There And Back Again).
- Other examples of property-based testing are: 1) verifying that something won't change, e.g. sorting a list shouldn't change its length, or 2) things that are hard to prove but easy to verify, such as that fields in a dictionary are never the empty string after you've called a data processing function.

## Final thoughts (talking head)

I've mainly talked about pretty low-level testing techniques in this video. In the coming months, I'm going to explore libraries in Python that can help you with setting all of these up and also look at all these different techniques in more detail. There are also higher level testing processes like integration testing or acceptance testing that also require a particular infrastructure such as a DTAP street (this stands for Development Testing Acceptance Production). I can talk about that stuff as well on the channel, let me know if want to know more about this. Also I'm curious: are you using unit testing at the moment? And what about mutation testing or property-based testing? Let me know in the comments below!

That's it for today - thanks for watching and see you next time!
