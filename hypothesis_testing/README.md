## Intro

## What is property-based testing?

Property based testing has become quite famous in the functional world. Mainly introduced by QuickCheck framework in Haskell, it suggests another way to test software. It targets all the scope covered by example based testing: from unit tests to integration tests.

Property based testing relies on properties. It checks that a function, program or whatever system under test abides by a property. Most of the time, properties do not have to go into too much details about the output. They just have to check for useful characteristics that must be seen in the output.

This is different from classical unit tests, which generally defines a fixture (predefined input value), runs a test using that fixture and then checks that the outcome is as desired.

Property-based tests are a different: although they also rely on example data, they test a property of the system by automatically generating various example data sets.

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

- Hypothesis has a ton of possibilities. I've only touched the surface here. For example, there are strategies for generating Numpy data structures or Pandas DataFrames, there are specific testing features for Django applications,
- Hypothesis even offers something called stateful testing, or model-based testing, where it doesn't just generate data, but it also generates tests. In this case you specify a number of primitive actions that can be combined, and then Hypothesis will try to find sequences of those actions that result in a failure.

- In my opinion a really powerful aspect of Hypothesis is the flexible data generation options. Overall, I think it's a really useful addition to your testing toolkit.

- Using a tool like Hypothesis is a good way to think more out-of-the-box about how you test your code. This doesn't mean you shouldn't write "normal" unit tests anymore. Depending on what you need to test, a regular, basic unit test can be just the right ticket. Remember that software design principles such as "keep things simple" also apply when you write test code.
