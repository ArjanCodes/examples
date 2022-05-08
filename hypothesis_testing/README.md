## Intro

## What is property-based testing?

## Different types of property-based testing

1. If you have a reversible operation (like encoding and then decoding a string), you can test that the operation and then the reversed operation result in the same value.

2. If you know that after calling a function, a certain property should hold, you can write tests to verify that as well.

The test_ascii example shows how to do these these things.

## Office: another example

- Show how test cases that fail are being shown and how they help
  a) fix generate_random_team accepting size <= 0
  b) fix the case where there's only the CEO
  b) what to do when generating an empty list?

## Strategies

One very powerful aspect of the hypothesis package is that it allows for a lot of flexibility in generating data.

- You can apply parameters to the built-in strategies
- You can build your own strategies, or create composites of strategies (see for example the composite employee_list)

- Show example of generating an employee list.
- Add minimum and maximum values to the list size.
