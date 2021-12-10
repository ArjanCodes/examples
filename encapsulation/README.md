# What is encapsulation

You might have heard other programmers use the word "encapsulation". What do they mean by that?

First meaning of encapsulation: Grouping related operations or things. The group exemplifies the essential features of something else, for example: "a culture document encapsulates a company's beliefs, values and practices".

Or in programming. A Customer class encapsulates the data that we consider to be essential for representing a customer. Or, an Order module encapsulates all relevant data and processes related to handling orders.

-- customer class example (without the send email stuff)

Even on a lower level, there's encapsulation. For example, a function is an encapsulation of the statements in its body.

So, in short, encapsulation is grouping things.

The second meaning of encapsulation is that you seal certain aspects of your code. So you provide an interface to that code using functions in a module, methods in a class, or even complete classes and modules that form a kind of capsule around the lower-level system. This means you're presenting a sort of black box that other parts of your program can use without them having to know anything about the inner workings. It's a mechanism to hide information, hide implementation details.

For example, let's say you have a payment processor, Stripe. You want to use it in your code but you don't want everything to directly depend on Stripe-specific things. So you encapsulate it. Create a StripePaymentProcessor class that has methods to start a payment process, process refunds, compute tax percentages, and so on. Inside it, you have implementation details such as knowing which API calls to make to Stripe specifically, authenticating to the Stripe service, extracting the data that you need from the response from the Stripe API, and so on. All the other parts of your code use the StripePaymentProcessor, but don't need to know anything about Stripe-specific things. Those are encapsulated. The information, the implementation details, are hidden. When you do this, the StripePaymentProcessor serves as a Facade, which is one of the design patterns in the Gang of Four book.

You can also hide information on a lower level, directly inside a module, or a class.

-- order class with set_payment_status method that hides the \_payment_status variable.

-- customer class with 'private' \_send_welcome_email method that's called when creating the customer.

But there's an elephant in the room. Python supports encapsulation in the sense that you can group things using functions or classes. However, the second meaning (information hiding) isn't strictly possible in Python. There are no access modifiers like other languages such as Java, C#, C++ or TypeScript have. I can't forbid somebody to call the \_send_welcome_email method in the Customer class. The accepted practice is to put an underscore in front of something that you're not supposed to use outside of its context, but you can't force it in Python.

The way I view it is that encapsulation means you're drawing a boundary around something. There's an inside and an outside. On the one hand, you're making a conceptual choice of where that boundary is drawn. That determines how you group data, what the input and output of your functions are, and what things are grouped in classes, in modules, in packages. Those are tools to draw those boundaries. The other choice you make as a software designer is which parts are going to hidden to other parts of your program. In Python you can't truly hide things, but you can encourage it using the underscore in front of variables, functions, methods, or even classes and modules to stress that those things belong to the inside part of the boundary and not the outside.

-- encapsulation with and without information hiding example

Encapsulation, pros and cons:

- to do
