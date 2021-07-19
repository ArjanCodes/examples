## About this video

This video is about test-driven development and the related concept of 'red-green-refactor'.

## Video outline

### Example explanation

This example is a simple `Employee` class that is used to compute how much someone should be paid based on their pay rate, the hours worked and a few more parameters.

I haven't implemented the `compute_pay` method yet. We're going to do that later and follow the process of test-driven development

### What is Test-driven development?

- Test-driven development (TDD, in short) is a term coined in 2002 by Kent Beck in his book "Test-driven development by example" (add link to description).

- Test-driven development has 5 steps:

1. Add a test
   The adding of a new feature begins by writing a test that passes iff the feature's specifications are met. The developer can discover these specifications by asking about use cases and user stories. A key benefit of test-driven development is that it makes the developer focus on requirements before writing code. This is in contrast with the usual practice, where unit tests are only written after code.
2. Run all tests. The new test should fail for expected reasons
   This shows that new code is actually needed for the desired feature. It validates that the test harness is working correctly. It rules out the possibility that the new test is flawed and will always pass.
3. Write the simplest code that passes the new test
   Inelegant or hard code is acceptable, as long as it passes the test. The code will be honed anyway in Step 5. No code should be added beyond the tested functionality.
4. All tests should now pass
   If any fail, the new code must be revised until they pass. This ensures the new code meets the test requirements and does not break existing features.
5. Refactor as needed, using tests after each refactor to ensure that functionality is preserved
   Code is refactored for readability and maintainability. In particular, hard-coded test data should be removed. Running the test suite after each refactor helps ensure that no existing functionality is broken.

**Repeat**
The cycle above is repeated for each new piece of functionality. Tests should be small and incremental, and commits made often. That way, if new code fails some tests, the programmer can simply undo or revert rather than debug excessively.

This process of writing failing tests first, then write the actual code, then improve the code is also called red-green-refactor. Let's add some tests to the example!

### Red

First, write the tests for the compute pay method. All new tests will fail.

### Green

Write the actual code and show in several steps that the tests are passing.

### Refactor

You realize that the Employee class can be improved. Actually, the `has_commission` Boolean variable can be replaced by a property that computes it based on the price paid per landed contract. Refactor this and adapt the tests.

### A few testing tips

- Don't use the same Employee instance in different tests.
- Don't test the Python built-in functions.
- Test by comparing with constant values, don't copy over the implementation.

### Why is test-driven development useful?

- Test-driven development offers more than just simple validation of correctness, but can also drive the design of a program. By focusing on the test cases first, one must imagine how the functionality is used by clients (in the first case, the test cases). So, the programmer is concerned with the interface before the implementation.

- Even though more code is required with TDD than without, the total code implementation time could still be shorter. Large numbers of tests help to limit the number of defects in the code. Fixing those defects early in the process usually avoids lengthy and tedious debugging later in the project.

- TDD forces you to write code that is flexible, extensible and modular, because you need to think about the software in terms of small units that are tested separately. Mocking (which I didn't cover in this video) helps as well because that requires modules to be able to be switched out easily.

### Caveats of test-driven development

- Writing and maintaining an excessive number of tests costs time. Also, more-flexible modules (with limited tests) might accept new requirements without the need for changing the tests. For those reasons, testing for only extreme conditions, or a small sample of data, can be easier to adjust than a set of highly detailed tests. In particular if the core of your software changes a lot (like in a startup), this is a big overhead.

- A high number of passing unit tests may bring a false sense of security, resulting in fewer additional software testing activities, such as integration testing and compliance testing.

- Unit tests created in a test-driven development environment are typically created by the developer who is writing the code being tested. Therefore, the tests may share blind spots with the code: if, for example, a developer does not realize that certain input parameters must be checked, most likely neither the test nor the code will verify those parameters. Another example: if the developer misinterprets the requirements for the module he is developing, the code and the unit tests he writes will both be wrong in the same way. Therefore, the tests will pass, giving a false sense of correctness.

### Takeaway

We've been adopting a TDD approach in my company and it's really pleasant to work in this way - I recommend you try it. Writing tests does take time. Especially in a startup you have to let go of trying to get a high coverage % in all cases. It's a balance between being able to ship something fast but buggy so your users can try it and give you useful feedback, vs perfect, bug-free code that takes a very long time to develop and you may scrap it after realizing it's not a useful feature. The nice thing with a technique like TDD is that you make that trade-off explicitly.

Hope you enjoyed this example. Thanks for watching, take care and see you next time!
