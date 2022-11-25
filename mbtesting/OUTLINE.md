## Introduction

- As developers, we like to automate things. At least I do!
- Writing software tests is a lot of work! So, in this video I’m going to cover a technique, model-based testing, or stateful testing, that you might like if you’re just as lazy as I am.
- Though model-based testing is not suitable for all your projects, if you can use it, it’s extremely powerful.
- This is a collaboration with Zac Hatfield-Dodds who is the main developer of the Hypothesis testing package.

## The example

- The example is a relatively simple order class with line items. You can add or remove line items and compute the total price. For performance reasons, the computed total is cached.
- There’s also a convenient method to update the quantity of a line item in the order. That’s something quite common if you’re building a web shop for example. As you can see, the code updates the cache accordingly.
- How would you write unit tests for this? Well, we’d have to think of the possible cases and write the tests for that ourselves.
- Show `test_order.py` as an example. Add post init method to Order since we forgot that.
- Problem: we have to think of a lot of cases ourselves, and things can get quite complex. It’s a hassle to have to write all those tests and make sure we don’t forget certain edge cases.
- This is where model-based testing comes in.

## What is model-based testing?

- Model-based testing, also called stateful testing, is a testing mechanism that relies on models to design and potentially also run software tests.
- You can approach this really formally. I’m not going to do that today, but instead focus on a practical application of this idea.
- How does model-based testing fit in and how is it different from other types of tests?
  - Traditional unit tests test exactly one input with an exact sequence of actions
  - Property-based tests test many inputs for an exact sequence of actions
  - Model-based tests let you explore many sequences of actions. In particular when you have multiple different methods that you can call, repeatedly and in multiple orders, it's impractical to hand-write tests for all of them. This is exactly the issue with the order example I showed before.
- If you use Hypothesis, what happens with model-based testing is that you Hypothesis choose what method to call next! And it’s built in.
- How does it work?
  - We start by listing all the available actions, for example: create a line item, add a line item to an order, remove a line item from an order; and sanity-checks for things that should always be true - for example the cached total.
  - Then, we'll define those as special methods in a class - the actions are "rules", and the things which are always true are "invariants".
  - When you run a model-based test, Hypothesis will repeatedly choose an action to run and execute that method, then run each of the sanity checks by executing all the invariant methods. So together, the rules and invariants form a state machine.
  - You can also add preconditions to any rule or invariant: for example, you can only remove an item if it's already in the order, or 'check that the total is zero, whenever the order is empty'
    - This would be well-motivated by raising an error instead of returning if the removed/changed line_item was not in the order

## Writing stateful tests for the Order example

- See the `test_order_stateful.py` example.
- There’s an `OrderTest` class that represents the state machine. In the initializer, it creates an Order object.
- You can also add state (= the information that a generated program keeps track of). This is called a Bundle in hypothesis. It allows to transfer data between rules. For example, you can create a line item in one rule, and add it to an order in another rule.
- When running the test, you now see that Hypothesis has found several edge cases we didn’t think of:
  - removing a line item from the order that wasn’t in the order
  - updating a line item quantity that wasn’t added to the order
  - adding the same line item twice to an order and then updating the total cache

## Final thoughts

- I think model-based testing or stateful testing is a really neat way of thinking about software testing. It’s suitable in particular when you have a situation where you have lots of possible action combinations and it’s cumbersome (and error-prone) to write all the tests manually.
- A few interesting things to know about Hypothesis:
  - Hypothesis is an early adopter of the PEP-654 ExceptionGroup type and PEP-678 exception notes, both new in Python 3.11 or via [https://pypi.org/project/exceptiongroup/](https://pypi.org/project/exceptiongroup/) , to improve error reporting.
  - Hypothesis integrates nicely with HypoFuzz, a tool that runs on your code and that checks for failures when passing it all sorts of malformed input.
  - Hypothesis also works with CrossHair. This is a tool that analyzes your code and if you use type annotations, you can specify postconditions that CrossHair is going to verify for you using Hypothesis under the hood.
  - Both HypoFuzz and CrossHair are tools that are intended to run for a longer time than just a basic suite of unit tests. And whatever they find will be added to the database so when you run your tests next time, it will instantly reproduce the failures.
