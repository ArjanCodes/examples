## About this video

In this video, I'll explain the difference between using inheritance vs composition and how that affects things like coupling and cohesion.

I've made an example about different employee types and reward structures to show how it works. In the first version (before.py), there is no inheritance, just three classes (= three employee types) with low cohesion (lots of responsibilities per class), and code duplication. Then there is a version that tries to solve those issues with inheritance (with-inheritance.py), and another version that uses composition (with-composition.py).

## Video outline

- Design principle "favor composition over inheritance". This is mentioned in the GoF design patterns book. What does it mean? Let's find out.

- What is inheritance? What is composition?

  - Both can help separate responsibilities
  - But watch out: inheritance leads to the strongest possible coupling

- Explain and analyze the basic example:

  - lots of code duplication
  - classes have too many responsibilities (storing personnel data, computing commission payments, computing other payments such as salary)

- Let's try inheritance

  - Create an Employee abstract base class containing name, id and an abstract pay method
  - Create different employee types (hourly, salaried, freelancer)
  - Now let's add commissions. We could add that to the Employee class, but that's not really clean: Employee is mainly concerned with employee data, and not payment-related things. Let add subclasses then for each employee type

- Analysis of the inheritance case

  - We did manage to separate storing personnel data from payments and commissions
  - Lots of classes and subclasses though, and if we add a new payment type or employee type, this leads to lots of extra classes (SalariedEmployeeWithCommissionAndBonus etc)
  - Commission code duplication

- How about composition?

  - Three classes: employee, contract, commission
  - Employee governs how payment overall is constructed from the parts
  - Three subclasses for contracts: hourly, salaried, freelancer
  - Patch everything up at the end

- Advantages of composition over inheritance:

  - No combinatory explosion of classes anymore
  - No more code duplication
  - Easily extendible with new contract types or new commission types

- Limitations of the example:
  - We could make commission an abstract class and create a ContractCommission subclass for better separation.
  - We could further separate the employee class into a EmployeePersonData class and an EmployeePayment class, because Employee is still responsible for both personal data and payment processes.
  - I used dataclasses, but perhaps a library like Pydantic is a better option, especially if you want to read employee data from a file.
