# What is encapsulation?

You might have heard other programmers use the word "encapsulation". Today I'm going to talk about what it means, why it's not the same as information hiding, and how you can use it to improve your design. Before we dive in, let's talk about this video's sponsor, Skillshare.

The first meaning of encapsulation is that we group things so that each group represents the essential features of something. For example, "a company's culture document encapsulates the company's beliefs, values and practices". Or, "a customer class encapsulates the data that we consider to be essential for representing a customer". Let's look at an example.

-- customer class example (without the send email stuff)

The second meaning of encapsulation is that is defines boundaries around things. For example, Han Solo was encapsulated in carbonite by Jabba the Hutt. I still have nightmares about that by the way. Or, you could be encapsulated in prison by the government for wire fraud.

So encapsulation in that sense is about restricting access. In your code, you can do that by defining protected or private instance variables or methods as protected or private. Even though Python is a bit special in that doesn't actually restrict access.

There's another aspect related to encapsulation, which is information hiding. This is slightly different. With information hiding, you hide certain aspects of your code from the outside. And then you provide an interface to that code using functions, classes, and modules that form a black box that other parts of your program can use without knowing anything about the inner workings.

For example, let's say you use a payment processor, Stripe. You want to use it in your code but you don't want everything to directly depend on Stripe-specific things. So you hide the information from the rest of the code. Create a StripePaymentProcessor class that has methods to start a payment process, process refunds, compute tax percentages, and so on. Inside it, you have implementation details such as knowing which API calls to make to Stripe specifically, authenticating to the Stripe service, extracting the data that you need from the response from the Stripe API, and so on. All the other parts of your code use the StripePaymentProcessor, but don't need to know anything about Stripe-specific things. The information, the implementation details, are hidden. When you do this, the StripePaymentProcessor serves as a Facade, which is one of the design patterns in the Gang of Four book.

Let's look at another example.

-- order class with set_payment_status method that hides the \_payment_status variable.

-- customer class with 'private' \_send_welcome_email method that's called when creating the customer.

What's really interesting is how encapsulation and information hiding are related to design principles. Encapsulation, providing boundaries, is closely related to cohesion. By encapsulating things, providing boundaries and grouping things together, you're making them more cohesive. Information hiding on the hand helps to reduce coupling. Information hiding removes dependencies by introducing abstraction layers. I did a video already quite a while ago, where I talk more about cohesion and coupling, I'll put the link here at the top. In short, both encapsulation and information hiding are going to help you improve your design by increasing cohesion and reducing coupling.

If you want to become better at design overall, and improve your decision making process, I've written a guide for you. It's available for free at arjancodes.com/designguide. It describes the steps I go through when I design a new piece of software. I've kept it short and practical, you can apply these ideas directly to your own projects. So, arjancodes.com/designguide. The link is also in the description of this video.

Before I finish this video, I want to show you one more example to clarify the difference between encapsulation and information hiding.

-- encapsulation with and without information hiding example

That last example is purely theoretical by the way, I would never advise you to write classes like this. Anyway, I hope you enjoyed this video and that it gave you some food for thought. If you did give it a like and consider subscribing to my channel if you want to learn more about software design and development. Thanks for watching, take care, and see you next time.
