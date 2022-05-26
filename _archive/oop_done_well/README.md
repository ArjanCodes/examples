# Intro (Talking head A)

"Object-Oriented Programming is bad, it leads to lots of boilerplate code and it's slow. Writing Object-Oriented code in Python is stupid, you're writing Java code in Python.". When I started this YouTube channel and posted a couple of my videos on Design Patterns on Reddit, these were some of the responses I got from the community. The comments weren't entirely off the mark. In those early videos I posted, there were lots of things to be improved, for sure.

For a while now, I've been going through a journey discovering how to use OOP well. Because OOP isn't bad per se. In this video I'm going to share 5 insights I got during that journey that will help you avoid some of the pitfalls and that will help you do OOP well. Sounds good?

Before I dive in, I have a free PDF guide for you. You can get it at arjancodes.com/designguide. It describes the 7 steps I take whenever I design a new piece of software. It's not about OOP in particular, but more about how to approach a software design problem and what you need to think about. If you enter your email address on the site, you'll get the guide in your inbox right away. To start, I want to give you a bit of background of where I'm coming from and how I've learned about OOP and how I've been using it in my own software development projects.

# My background (Talking head B)

When I started studying CS, in 1995, Java just appeared on the scene. It wasn't yet part of my curriculum in my first and second year (I learned Modula-2 and C++), but very quickly, the entire education sector changed to Java. In some sense, Java encapsulates the worst of OOP. It's verbose, you can't not use a class in your program. So it invites you to write really complex programs and structures. It was quickly adopted by businesses to write very complex designs with deep inheritance hierarchies, very long class names, and overly complex software structures fed by complex design processes involving many stakeholders (Waterfall, Rational Unified Process). I still see some teachers in CS doing this with Java and I think it's for a big part responsible for the hatred against OOP.

After I finished my studies, I moved to Switzerland to do a PhD in Computer Graphics. I was using a lot of C++ in those days because it was more efficient than Java though I did develop a car accident simulation program in Java3D as well. I also used quite a bit of Python, but I mainly used it to script animations and control the graphics engine, which itself was written in C++.

When I moved back to the Netherlands to teach CS, I switched to C# and Python as my main languages of choice for teaching students how to program and how to design software. And then when I started my own company 5 years ago, I switched again, but then to JavaScript and very quickly Typescript. I'm not teaching at the university anymore. I view this YT channel as a more modern way of teaching that allows me to help more people than just the students in my class.

# Towards functional programming (Talking head A)

Over the years I've moved from writing purely OOP code towards functional programming. This is also because I've been developing a lot of software using React and Typescript. Typescript has great support for functional programming, and modern React relies a lot on functional components. So moving to functional programming came quite naturally to me.

You may have seen part of this shift in my YT videos over the last year. It doesn't mean I don't like OOP though. Used carefully, classes can really help you write cleaner, more readable code. So, here are 5 things that I learned about OOP

# Insights for OOP done well

1. There's no need to only use OOP or only use hardcore functional programming. Use whatever results in the most readable code. And that's certainly not always purely functional programming with no state whatsoever. Especially in Python, we don't have to choose between OOP and functional. We can use a combination of both. Let's look at an example.

2. Make your classes either behavior-focused (mainly acting as a group of methods/behavior), or data-focused (representing a structured collection of data with not too many methods in the class).

3. The more you use inheritance, the more complication you add to your program. Mixins make things even worse because you inherit from multiple classes (and there are a bunch of other reasons why using mixins is a really bad idea). I generally only use inheritance in the sense that I define interfaces using either ABCs or Protocol classes and then inherit from the ABCs (Protocols don't have an inheritance relationship). The classic design patterns follow this same principle: very lightweight inheritance, mainly rely on composition.

4. Use dependency injection to make connections between objects (composition). In general I don't let objects create other objects, because it leads to code that's harder to test. Ideally, there should be a single place in your code that contains the 'dirty details'.

5. Python has a lot of 'magic methods' to change the way that classes and inheritance works. It may be tempting to use this to customize your code, but I really recommend against doing that. If other developers have to use your code, they will have certain assumptions about how things work. By changing the way classes and inheritance works, your code behaves in a non-standard way, leading to surprises and unexpected behavior.

I hope you enjoyed this video. If you did, give it a like and consider subscribing to my channel to learn more about software development and design. Thanks for watching, take care, and see you soon.
