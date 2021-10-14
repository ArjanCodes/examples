## Video outline

I did several videos covering code smells in the past. If you haven't watched those yet, I'll put a link to the previous two videos in the description. Some of you told me you don't like the word code smell. So here's a warning: please skip the following 10 seconds. Code smell, code smell, code smell, code smell, code smell, code smell, code smell! 7! That's how many I'm going to cover in this video. And there's a smelly little bonus at the end. While I'm working on the code today, I'll be using Tabnine, this video's sponsor.

## Tabnine sponsored section

## Explain the example (screencast)

Example of a Point-Of-Sale (POS) system for handling orders.

## What are code smells? (talking head)

Recap: a code smell is not a bug, it's more of a hint that something's wrong in your code. It can be a minor thing that's easy to fix. Or, it can point to a bigger problem in your design. Today, I'll cover 7 more code smells. Not all of them are Python-specific by the way. But regardless, they're still pretty smelly! Now, time to clean up this code.

## Code smell #1: Wrong/too elaborate data structure

Order is using various arrays to store items, quantities and prices. This leads to problems because we have to keep track of three arrays and make sure they're the right size. It makes more sense to combine an item, a quantity and a price into an object. Let's call that a line item and add a separate class for it.

## Code smell #2. Misleading names

It's hard to name things. Methods are often called add_something, create_something, get_something, etc. Are we really adding something? Or creating it? Or getting it? It's important to have method names reflect what the method actually does. In this case, the create_line_item method should be called add_line_item, since it's adding something to a list, not creating something for us.

## Code smell #3. Classes with way too many instance variables

Order contains lots of instance variables. When a class contains too many instance variables, this is often a sign that the class has too many responsibilities. In this case, order is responsible for store line items, as well as customer details. To improve this, we can separate the customer details out into a separate class Customer.

## Code smell #4. VerbSubject / Ask Don't Tell ([https://wiki.c2.com/?VerbSubject](https://wiki.c2.com/?VerbSubject)):

Whenever you encounter a method that gets a single object as a parameter and then does something with that object and nothing else, this is called the VerbSubject smell (the method name is the verb, the subject is the object). The positively worded principle is: "ask don't tell". Instead of asking for details and performing a computation yourself, simply ask the object to do it. An example is compute_total_price in POSSystem. In many cases, this means that the method should actually belong to the object it's doing something with. In this case, we can move compute_total_price to Order. Let's also turn it into a property, and call it total_price and do the same in LineItem to make computing the total price even simpler. You can still use a for-loop in total_price, but you can also sum, which simplifies the code to a single line.

## Code smell #5. Backpedalling / Law of Demeter ([https://wiki.c2.com/?BackPedalling](https://wiki.c2.com/?BackPedalling)):

Backpedalling means that you call a method, but then not provide the data it needs, so that the method needs to find all the stuff it requires elsewhere, often leading to the method needing implemenation details of another object. A related principle is the Law of Demeter: the principle of least knowledge. You see this happening in the payment processor, which has to get all kinds of information from the POSSystem when it processes a payment. If you look at what the payment processor actually needs it's only two things: a price that needs to be paid, and a reference or id related to what you're paying. So let's simply provide those things to the process_payment method, and make payment processor completely independent of the POS system.

## Code smell #6. Hardwired sequences with a single order:

Currently, we need to make sure to initialize the payment processor connection explicitly, otherwise it breaks. In general, there's probably not a single use-case where we don't want to initialize the payment processor before we use it, so it's better to do this automatically. You could simply move initialization stuff to the class initializers, but unfortunately this is not always possible. For example, if you rely on an asynchronous operation, like establishing a database connection or opening a websocket, you can't do this in a class initializer, because those are not asynchronous. What you can do is make sure that the extra work you need to do only happens in a single place. Now you need to do something extra in the POS System as well as in the main file. Let's change this to let the main file do this work and leave it out of the POS system, and then use dependency injection to provide the payment processor to the POS system once it's been initialized. Using dependency injection here has as an additional example that POSSystem is now easier to test, since it doesn't create it's own payment processor anymore, but you could inject a stub yourself when you're testing the class.

## Code smell #7. Comments

Finally, this is not really a code smell, but more of a general guideline. Where to put comments? If you use Pylint and leave it on the default setting, it's going to complain that you need to add a comment to each module, class, method and function. In my opinion, this is overkill. In some of my previous videos I followed Pylint's default settings, but it lead to way too much useless comments everywhere. So here's a tip. Use comments to describe what a module or a class does. If a module only contains a single class, then put a comment either at the module or at the class level, both is not needed. Don't have comments at the top of methods or functions, but use clear names (see code smell 2 of this video), so you always understand what a function or method does. Use single line comments in the function body to clarify aspects of the code as needed. Write those comments at the start of the line, not behind a line of code. If you need too many comments, you probably need to split the function or methods into separate parts to increase clarity.

## BONUS Code smell. Clarify function calls with keyword arguments

When you call a function that has more than a single parameter, use keyword arguments to clarify what each argument is. As an example, take the customer class or the line item class: you can use keyword parameters here to improve the clarity of the code.

## Final thoughts

A note about dataclasses. They help reduce boilerplate so you don't have to write explicit initializers. The onyl issue is that they potentially decrease encapsulation, because you might want to directly access and modify the objects. You can combat this by adding methods to classes to do that job for you. For example, the Order class has a set_status method while you could just as well directly modify the status.

Most of the code smells in this video were not really Python-specific, so you can apply these to any programming language. I hope you enjoyed this code smell video. Thanks again to the sponsor of this video, Tabnine, check them out via the link in the description. Thanks for watching, take care and see you next time!
