There’s a set of design principles called GRASP. If you apply these principles to your code, you’re going to dramatically improve the quality. What’s also nice about them is that they don’t just apply to object-oriented code, like the SOLID principles, and that makes them really helpful if you’re writing Python code.

## Overview

- GRASP is the abbreviation of General Responsibility Assignment Software Patterns (or Principles).
- Set of nine fundamental principles in object-oriented design
  - Creator
  - Information expert
  - Controller
  - Indirection
  - Low coupling
  - High cohesion
  - Polymorphism
  - Protected variations
  - Pure fabrication

## 01 - Creator

- The creator principles help us to decide which class should be responsible for creating instances of another class.
- So, assign class B the responsibility for creating instances of another class A if some of these are true:
  1. Instances of **B** contain or compositely aggregate instances of **A**
  2. Instances of **B** record instances of **A**
  3. Instances of **B** closely use instances of **A**
  4. Instances of **B** have the initializing information for instances of **A** and pass it on to creation. In other words, B is the information expert of A, leading to the next principle.
- Code examples: `01-creator_before.py` and `01-creator_after.py`
  - This code contains 3 classes: `Sale`, `SaleLineItem` and `ProductDescription`.
  - The two instances of `SaleLineItem`, `row1`, and `row2`, were created at the `main` function.
  - The creator principles tell us that it should be created in class `Sale` because it follows the (1) in the creator definition: class `Sale` store records of `SaleLineItem`. Therefore, `Sale` should be the class that has the responsibility to create instances of `SaleLineItem`
  - A method `add_line_item` is created in `Sale` to produce an instance of `SaleLineItem` and append it to the `Sale.items` attribute.

## 02 - Information expert

- This principle helps to decide where to assign new responsibilities for objects.
- Assign responsibilities to the ****************\*\*\*\*****************information expert****************\*\*\*\*****************, in other words, the class with the information necessary to fulfil the responsibility.
- Code examples: `02-information_expert_before.py` and `02-information_expert_after.py`
  - This code contains 3 classes: `Sale`, `SaleLineItem`, and `ProductDescription`.
  - In which class should be implemented the ************************\*\*\*\*************************total price of a sale?************************\*\*\*\*************************
    - The answer is guided by the question: which class has all the information, in other words, which class is the information expert, in order to calculate them?
    - The ************************\*\*\*\*************************total price of a sale************************\*\*\*\************************* can’t be allocated in `ProductDescription` because the class doesn’t know any information about the `SaleLineItem` associated with it. The `SaleLineItem` class is only aware of itself and doesn’t have any information about the other items.
    - According to the information expert principle, the ************************\*\*\*\*************************total price of a sale************************\*\*\*\************************* should be allocated to the `Sale` class because it has all the information needed, looking at all `SaleLineItem` with quantities and product prices. The `Sale` is the information expert on the ************************\*\*\*\*************************total price of a sale.************************\*\*\*\*************************
  - In which class should the ************************\*\*\*\*************************total price of a sale line item************************\*\*\*\************************* be implemented************************\*\*\*\*************************?************************\*\*\*\*************************
    - The same principle of finding which class is the information expert is applicable here.
    - The `ProductDescription` class doesn’t know about the number of items bought
    - The `Sales` class knows all of the prices and quantities, but this is too much information for just one line of sales in an invoice, for example.
    - The `SaleLineItem` should be the information expert in this case. The ************************\*\*\*\*************************total price of a sale line item************************\*\*\*\************************* is allocated to it according to this principle.

## 03 - Controller

- Non-user interface object responsible for receiving or handling a system event.
- Defines the method for the system operation.
- When a request comes from a user-interface layer object, it helps us determine what is the first object that receives the message from the UI layer objects.
- Code examples: `03-controller_before.py` and `02-controller_after.py`
  - The general idea of code is to implement a GUI to add and remove products.
  - SQLite is used as the database
  - The before version doesn't have a `Controller` class, meaning that the `App` class handles the interface layout generation and also the actions coming from users.
  - In the after version, a `Controller` class is added in order to be responsible for handling the actions, when a button is clicked, for example. All those methods are moved from `App` to `Controller`.

## 04 - Protected variations

- Design objects, subsystems and entire systems so that the variations or instabilities in these elements do not have an undesired impact on other elements.
- Code examples: `04-protected_variations_before.py` and `04-protected_variations_after.py`:
  - The before example is exactly the same as `04-controller_after.py`
  - To decouple the `App` and `Controller` classes, the `AppInterface` protocol was introduced.
  - The `Controller` class now depends on just an interface and it’s protected against variations in `App` class.

## 05 - Indirection

- Introduces an intermediate unit to communicate with the other units, so that the other units are not directly coupled.
- Avoid a direct coupling between two or more elements.
- The main benefit is low coupling
- It can be achieved with several well-known design patterns: Adapter, Facade or Observer.
- Code examples: `05-indirection_before.py` and `05-indirection_after.py`:
  - `Customer` and `Order` are coupled directly. The `Order` needs to retrieve discount information from `Customer`
  - An intermediate-class `Discount` is introduced to reduce the direct coupling between `Customer`

## 06 - Low coupling

- Comes in order to support low dependency, low change impact, and increase reuse
- Assign a responsibility so that coupling remains low.
- A class, for example, with high (or strong) coupling relies on many other classes. Such classes may be undesirable; some suffer from the following problems:
  - Forced local changes because of changes in related classes.
  - Harder to understand in isolation.
  - It is harder to reuse because its use requires the additional presence of the classes on which it depends.
- Code examples: `06-low_coupling_before.py` and `06-low_coupling_after.py`:
  - The `total_discounted_price` is a bad example of high coupling because it depends on both `Cash` and `CreditCard`
  - The problem was solved by introducing a `PaymentMethod` protocol and both `Cash` and `CreditCard` followed it.
  - The `total_discounted_price` now depends only on a protocol that obligates any other payment methods to follow it.

## 07 - High cohesion

- Narrow the responsibilities of classes to keep them focused, understandable and manageable.
- Applying high cohesion brings the side effect of supporting low coupling, which is an advantage.
- To achieve high cohesion:
  - Refactor to break up classes into more well-defined responsibilities.
  - Avoid classes that have too many responsibilities (”God classes”).
- Code examples: `07-high_cohesion_before.py` and `07-high_cohesion_after.py`:
  - Example reworked from the \***\*[Cohesion and coupling: write BETTER PYTHON CODE Part 1](https://www.youtube.com/watch?v=eiDyK_ofPPM&t=1185s)** vídeo (2021).
    - Applied some recently adopted best practices at the newest videos (type hints, enum classes instead of strings, docstrings insertion, main function definition, etc.)
  - “God class” `Application` with one “god method” that makes everything.
  - The `Application` class was split into three others: `VehicleInfo`, `Vehicle` and `VehicleRegistry` for a well splitting of responsibilities.

## 08 - Polymorphism

- The principle is also present in Gang of Four Design Patterns (GoF)
- Assign responsibility for the behaviour using sub-classes from a defined interface.
- Very useful to refactor long **\*\*\*\***if-else**\*\*\*\*** statements based on types
- It’s totally compliant with the open-close principle from SOLID.
- Code examples: `08-polimorphism_before.py` and `08-polimorphism_after.py`:
  - The **\*\*\*\***if-else**\*\*\*\*** statement of the `convert` method in the `Converter` class was replaced by a `Formula` abstract class with its respective subclasses: `InchesToCentimeters`, `MilesToKilometers` and `PoundsToKilograms`.

## 09 - Pure fabrication

- Create new classes with a well-defined responsibility when there are no good choices
  - They are applied when there is no such other good **information expert** class to handle new methods.
- An example would be a `Payment` class and the desire to store the payment transaction.
  - The new class `PersistentStorage` would be created in order to deal with it.
  - Other types of storage could be created afterwards without affecting the `Payment` class.
- This is often achieved by using factor classes.
- Code examples: `09-pure_fabrication_before.py` and `09-pure_fabrication_after.py`:
  - There is one single-class `Payment` that is responsible for processing payments and storing records.
  - Two other classes, `PersistentStorage` and `PaymentHandler` were created in order to better split responsibilities.
  - `PersistentStorage` has a single well-defined responsibility: dealing only with payment records.
  - `PaymentHandler` is responsible for applying the entire payment process and storing it at the end.
