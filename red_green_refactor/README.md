## About this video

This video is about test-driven development and the related concept of 'red-green-refactor'.

## Video outline

### Example explanation

This example is a simple `Employee` class that is used to compute how much someone should be paid based on their pay rate, the hours worked and a few more parameters.

I haven't implemented this method yet. We're going to do that later and follow the process of test-driven development

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

This process of writing failing tests first, then write the actual code, then improve the code is also called red-green-refactor.

### Red

First, write the tests for the compute pay method. All new tests will fail.

### Green

Write the actual code and show in several steps that the tests are passing.

### Refactor

You realize that the Employee class can be improved. Actually, the `has_commission` Boolean variable can be replaced by a property that computes it based on the price paid per landed contract. Refactor this and adapt the tests.

### Why is test-driven development useful?

Programmers using pure TDD on new ("greenfield") projects reported they only rarely felt the need to invoke a debugger. Used in conjunction with a version control system, when tests fail unexpectedly, reverting the code to the last version that passed all tests may often be more productive than debugging.[12]

Test-driven development offers more than just simple validation of correctness, but can also drive the design of a program.[13] By focusing on the test cases first, one must imagine how the functionality is used by clients (in the first case, the test cases). So, the programmer is concerned with the interface before the implementation. This benefit is complementary to design by contract as it approaches code through test cases rather than through mathematical assertions or preconceptions.

Test-driven development offers the ability to take small steps when required. It allows a programmer to focus on the task at hand as the first goal is to make the test pass. Exceptional cases and error handling are not considered initially, and tests to create these extraneous circumstances are implemented separately. Test-driven development ensures in this way that all written code is covered by at least one test. This gives the programming team, and subsequent users, a greater level of confidence in the code.

While it is true that more code is required with TDD than without TDD because of the unit test code, the total code implementation time could be shorter based on a model by Müller and Padberg.[14] Large numbers of tests help to limit the number of defects in the code. The early and frequent nature of the testing helps to catch defects early in the development cycle, preventing them from becoming endemic and expensive problems. Eliminating defects early in the process usually avoids lengthy and tedious debugging later in the project.

TDD can lead to more modularized, flexible, and extensible code. This effect often comes about because the methodology requires that the developers think of the software in terms of small units that can be written and tested independently and integrated together later. This leads to smaller, more focused classes, looser coupling, and cleaner interfaces. The use of the mock object design pattern also contributes to the overall modularization of the code because this pattern requires that the code be written so that modules can be switched easily between mock versions for unit testing and "real" versions for deployment.

Because no more code is written than necessary to pass a failing test case, automated tests tend to cover every code path. For example, for a TDD developer to add an else branch to an existing if statement, the developer would first have to write a failing test case that motivates the branch. As a result, the automated tests resulting from TDD tend to be very thorough: they detect any unexpected changes in the code's behaviour. This detects problems that can arise where a change later in the development cycle unexpectedly alters other functionality.

### Caveats of test-driven development

Test-driven development does not perform sufficient testing in situations where full functional tests are required to determine success or failure, due to extensive use of unit tests.[19] Examples of these are user interfaces, programs that work with databases, and some that depend on specific network configurations. TDD encourages developers to put the minimum amount of code into such modules and to maximize the logic that is in testable library code, using fakes and mocks to represent the outside world.[20]

Management support is essential. Without the entire organization believing that test-driven development is going to improve the product, management may feel that time spent writing tests is wasted.[21]

Unit tests created in a test-driven development environment are typically created by the developer who is writing the code being tested. Therefore, the tests may share blind spots with the code: if, for example, a developer does not realize that certain input parameters must be checked, most likely neither the test nor the code will verify those parameters. Another example: if the developer misinterprets the requirements for the module he is developing, the code and the unit tests he writes will both be wrong in the same way. Therefore, the tests will pass, giving a false sense of correctness.

A high number of passing unit tests may bring a false sense of security, resulting in fewer additional software testing activities, such as integration testing and compliance testing.

Tests become part of the maintenance overhead of a project. Badly written tests, for example ones that include hard-coded error strings, are themselves prone to failure, and they are expensive to maintain. This is especially the case with fragile tests.[22] There is a risk that tests that regularly generate false failures will be ignored, so that when a real failure occurs, it may not be detected. It is possible to write tests for low and easy maintenance, for example by the reuse of error strings, and this should be a goal during the code refactoring phase described above.

Writing and maintaining an excessive number of tests costs time. Also, more-flexible modules (with limited tests) might accept new requirements without the need for changing the tests. For those reasons, testing for only extreme conditions, or a small sample of data, can be easier to adjust than a set of highly detailed tests.

The level of coverage and testing detail achieved during repeated TDD cycles cannot easily be re-created at a later date. Therefore, these original, or early, tests become increasingly precious as time goes by. The tactic is to fix it early. Also, if a poor architecture, a poor design, or a poor testing strategy leads to a late change that makes dozens of existing tests fail, then it is important that they are individually fixed. Merely deleting, disabling or rashly altering them can lead to undetectable holes in the test coverage.

### Final thoughts

Hope you enjoyed this example. Thanks for watching, take care and see you next time!
