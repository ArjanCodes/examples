# Unit testing example

In this video, I'm going to take you through writing unit tests for existing code and show you the kinds of things you encounter while doing that. I'll also show you how unit tests help you refactor your code and design it better.

In a perfect world, you would be following TDD. But sometimes, you have to deal with existing code that's not properly tested.

# Explain the example

It's a simply Point-of-sale system with an order and a payment processor (I've used this example before).

# Order and LineItem tests (after version)

These are pretty easy to do, add a few different tests to cover different cases (like an empty order, line item with quantity 1 or more, ...)

# Processor tests

Not that hard either, but we do need a valid API key here otherwise the processor doesn't work. I'll show you how to deal with this in the test of the payment function

# Payment tests

This becomes a lot harder now. We need to mock the input. And to solve the issue with the API key, we also need to mock PaymentProcessor methods, because we depend on a "live" payment processor here.

Often when you mock things, this is a sign that there's an issue with the design of your code. Let's try to refactor this code to simplify how we can test this code, leading to a better design as well.

# Processor tests (after_refactor version)

- Move the API key value out of the code
- Change the luhn algorithm to a function (it doesn't need to be part of the payment processor)
- Compute the date dynamically to make sure the test keeps working in the future as well

# Payment tests

- Create a PaymentProcessor protocol class
- Create a PaymentProcessorMock class to handle the charge

# Final thoughts

- Always be careful that you're testing the right things in the the right place. For example, in test_payment, we don't want to test things related to valid or invalid credit card since that's part of the processor tests.
