# The ultimate guide to writing great functions

Writing great, well-designed functions is hard and takes a lot of practice. I’m going to cover the 7 most important things you should do when writing functions. Over the past years, I’ve seen a lot of code by different people. Code written by some of the students following my online course or code written by a development team in a company that’s actually used in a production environment. Almost none of the code that I’ve seen applied everything that I’m going to cover today. If you do apply all these things consistently, it’s going to completely change the way you write code from now on.

There’s a lot of ground to cover, so let’s dive in.

## 1. Do one thing and do it well

Your function should do a single task. But some time while doing a single task we indirectly do other sub tasks also. So the question is are we breaching the rule in that case? The answer might be No if we have maintained the same level of abstraction inside that function.

As I mentioned above, a function should do a single task. In general, function should change the state of an object or it should return some information about that object, not both.

In the example, there are several problems with the `validate_card` function. Most importantly, the function does too many different things:

- It computes the Luhn checksum
- It checks the validity of the card number and returns the result
- It changes the Customer object with that result

That’s three different things, way too many. And there’s another problem with this function that I’ll touch on in a minute. We can already improve this function a lot by splitting out the Luhn checksum computation from the rest of the code.

**Split out the Luhn checksum computation from the validate_card function.**

## 2. Separate Commands from Queries

The next two points are spin-offs of the first point. The `validate_card` function still does too many things. In particular, it retrieves some information (whether the credit card is valid) and it perform an action (it modifies the customer).

In general, make sure that a function either retrieves information (does a query) or performs an action (a command), but not both. This is a principle called the Command-Query Separation principle, which was thought by Bertrand Meyer, he’s French. He’s the one who came up with the idea of Design by Contract, he originated the Open-Closed Principle and he also created a programming language called Eiffel. Of course, he’s French. Makes a lot of sense. What doesn’t make sense at all is that a Dutch guy created a programming language called Python. There are no Pythons in the Netherlands! He should have called it Tulip. Or Cheese. Or Prostitute. It’s a missed opportunity.

def update_item_matching(thing): # update some item that lives in a collection
for item in collection:
if matches(item, thing):
update(item)
break

**Make the function only return a value and store it in the customer object in the main function.**

## 3. Only request information you actually need

- It doesn’t need the full customer information to do this job it also gets too much information (this is also called inappropriate intimacy).
- A simple way to fix this is by splitting out the arguments so the function no longer relies on a Customer object.
- There are other ways to fix this that I’ll touch on in a minute.

**Change the validate_card function to have three parameters with the card data instead of a single Customer object. Extra tip: if your function has multiple arguments, a great way to make your function clearer is by forcing the use of keyword arguments. You can use the asterisk in Python for this.**

## 4. Keep the number of arguments minimal

It is always a good practice to keep arguments to a function minimum. Because it demands a lot of conceptual power if we use many arguments. It is more harder from testing point of view also. Out argument is even more confusing because we do not usually expect information to be going out through the arguments.

- One way to solve this is by using abstraction with for example a Protocol class. If we go back to passing the customer object, we can introduce a Protocol class to not make the function directly dependent on the Customer type anymore. And now it only needs a single parameter.
- Another thing you can do is to better structure your data. For example, we can decide to put the credit card information into a separate card object. You can even decide to keep the Protocol class around if you like.

**Change the function to accept a CardInfo protocol. Then you can still pass the customer and not have the dependency. Then, introduce a Card class and pass that instead of the customer.**

## 5. Don’t create and use an object at the same time

Take a look at the Payment Processor example. Currently, the `order_food` function creates a payment handler and also uses it to handle the payment. The function is now directly dependent on a very specific payment handler. If you want to replace this by for example PayPal, you’d have to dive into the implementation and change a lot of this (and by the way, avoid PayPal if you can - unless you like API hell). It also makes the function hard to test, because now you need to patch the `StripePaymentHandler` object somehow before you can test the function.

To solve this, use dependency injection to provide the object that the function uses. This also makes testing the function a lot easier. An even better approach is to also introduce abstraction. This way, you can turn dependency injection into dependency inversion. This makes testing the code even easier, because you can easily create your own mock object to replace the Stripe payment handler as long as it follows the interface that you specified.

A little bonus tip for you: don’t order fries, order a salad. It makes you think more clearly.

**Change the payment processor code to use dependency injection first. Then, introduce a Protocol class to provide decoupling.**

## 6. Don’t use flag arguments

If you see a function that has a flag argument, that’s a serious “red flag”. Most often, it means that the function actually does two things: one thing when the flag is true and another thing when the flag is false. Not always, there are cases where a flag is simply a setting that’s passed along. But in many cases, it’s better to split up the function.

Here’s an example of an `Employee` class with a single method that has a boolean flag. The method actually does a completely different thing depending on the value of the flag. If the flag is true, the second argument isn’t even used. Let’s split this up into two functions, which makes the code much clearer.

**Split up the take_a_holiday method into two methods.**

## 7. Remember that functions are objects

Because like anything else in Python, functions are objects, you can compose them in different ways, leading to interesting patterns that are generally shorter than if you would implement those same patterns using object-oriented programming. A function can get another function as an argument, a function can even return another function.

- You can turn the PaymentHandler into a single function, and then `order_food` expects a function as an argument. To specify the type, use `Callable`.
- If you order food and pay with Stripe in several places in your code, you can use **partial function application**. Partial gets a function as an argument + any argument value of that function, and then it returns a new function, with those argument values already applied.

**Change the PaymentHandler into a function and use a type alias. Then, show how you can use partial to create a new function that already has the payment handler applied to it.**

## BONUS: Tips for naming functions and arguments

Here are a few quick bonus tips related to naming functions (good naming is really important):

- If a function has “and” in the name, check that the function does one thing. Names like `create_user_and_store_in_db` or `register_and_send_welcome_email` are red flags. These functions should probably be split up.
- Choosing good argument names helps with readability and allows your function name to be shorter in some cases. For example, `publish_info_to_library(lib)` can be shortened to `publish_info_to(library)`.
- Function names should be actions (there should be a verb in there) and arguments should be nouns. So, instead of `greeting(say_hi_to: str)` use `greet(name: str)`.
- Make sure you use the same vocabulary everywhere. If you call something an `article` somewhere, don’t call it a `story` or an `essay` somewhere else. If you call a collection of articles a `library`, use that everywhere, don’t use `l` or `lib` in half of the places and `library` everywhere else.
- Use the naming scheme that the language prescribes. In case of Python, it’s snake case, not camel case. I’m looking at you PyQt.
- And finally, make sure there are no typos or grammar issues in your function names. Is especially frustrating if you’re a grammar nazi like myself to have to use `is_memebr`or `are_order_paid`. And then you actually have to type that when you call the function. Ugh.

Hope you enjoyed this video. If you want to dive deeper into what you can do with functions in Python, watch this video next, where I dive deeper into what you can do with Python’s `functools` package. It changed the way I write code.
