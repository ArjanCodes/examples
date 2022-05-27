## Intro

Testing your software is really important. At least, if you want happy customers. There's a lot of different ways to test software, in particular, it's quite common to start with writing unit tests. Unit tests are great, but writing them is a lot of work. And the bigger your codebase becomes, the more time you have to spend writing and maintaining your tests. It's not uncommon that the testing code is more lines than that actual application code. And if you're not careful, developing and releasing new features is going to become really hard, to a point where you feel like even a minor change is going to involve a lot of development work.

There might be a way out of this, by looking at other ways to test software. One in particular that I find really interesting is property-based testing. I'm going to show you how to do this in Python, using the honestly, awesome Hypothesis package.

Before we dive in, I have something for you. It's a free guide that helps you design new software from scratch. You can get this at arjancodes.com/designguide. It contains the 7 steps I take whenever I design a new piece of software. If you enter your email address on the site, you'll get the free PDF in you inbox right away. So, arjancodes.com/designguide. The link is also in the description of this video.

## What is property-based testing?

A unit test, generally defines a fixture (a predefined, specific input value), runs a test using that fixture and then checks that the outcome is as expected.

Property-based testing checks that a function, program or any system abides by a property. Most of the time, property tests don't need to know that much about the specific inputs or outputs of a system, they just check specific characteristics.

Although property-based tests also rely on example data like unit tests, they're different because they test a property of the system by automatically generating example input data.

Property-based testing is quite well-known in functional programming. It was introduced by the QuickCheck framework in Haskell. You can use this testing approach on all levels of example-based testing: from unit tests to end-to-end tests.

## Different types of property-based testing

There are all kinds of different properties you can test. For example:

1. If you have a reversible operation (like encoding and then decoding a string), you can test that the operation and then the reversed operation result in the same value.

2. You can test properties of data that the code that you're testing is manipulating. For example: you can test that a sorting function you wrote doesn't change the length of the list that you sort. In this case you're testing the list length property.

3. Another property you could test is that the result of a function call adheres to some condition. For example, if you are testing a function that generates UUIDs, you can check that the generated id follows the UUID structure.

I'm going to show you two different examples now where property-based testing helps write better tests.

## Show the test_ascii example (screencast)

## Show the office example

REVIEWERS: I start with office_before.py which contains a few bugs, and then use hypothesis to define a property test for generate random team, and then for fire random employee. Hypothesis will show two bugs. One is that generate random team accepts a size <= 0 leading to issues. Second is that if fire random employee doesn't work correctly if the only employee is the CEO

- Show how test cases that fail are being shown and how they help
  a) fix generate_random_team accepting size <= 0
  b) fix the case where there's only the CEO (using generate_random_team directly in test_fire_employee)

## Strategies

One very powerful aspect of the hypothesis package is that it allows for a lot of flexibility in generating data.

- You can apply parameters to the built-in strategies (min and max value)
- You can build your own strategies, or create composites of strategies (see for example the composite teams in test_office)

- Show example of generating an employee list.
- Add minimum and maximum values to the list size.

## Let Hypothesis write the tests for you!

If you run these commands:

hypothesis write office.generate_random_team > test/generated/test_office_1.py
hypothesis write office.fire_random_employee > test/generated/test_office_2.py

Hypothesis will create basic tests for you that actually makes sense (REVIEWERS: the generated files are in the repository under test/generated)

## Final thoughts

Overall, I think Hypothesis is a really useful addition to your testing toolkit. It has a ton of possibilities and I've only touched the surface in this video. I have a few final thoughts.

- A really powerful aspect of Hypothesis is the flexible data generation options. For example, there are strategies for generating Numpy data structures or Pandas DataFrames, there are specific testing features for Django applications. You can even imagine that the data generation system can be helpful for other things than testing, for example if your application needs to generate random selections of things with specific conditions.

- Hypothesis also offers something called stateful testing, or model-based testing, where it doesn't just generate data, but it also generates tests. In this case you specify a number of primitive actions that can be combined using a flow chart, and then Hypothesis will try to find sequences of those actions that result in a failure. It's definitely something I want to dive into more. Let me know in the comments if you have any experience with this that you'd like share.

- Using a tool like Hypothesis is a good way to think more out-of-the-box about how you test your code. This doesn't mean you shouldn't write "normal" unit tests anymore. Depending on what you need to test, a regular, basic unit test can be just the right ticket. Remember that software design principles such as "keep things simple" also apply when you write test code.

If you want to get started writing unit tests for your code and do it in such a way that you improve the design of your code as well, watch this video series where I show you exactly how to do this.
