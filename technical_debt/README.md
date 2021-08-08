## About this video

This video is about managing technical debt.

## Video outline

- Start with showing the AH plastic coin for shopping carts. This... is technical debt! If you're Dutch, you know what this is. You can put this into a shopping cart to unlock it. But it's also technical debt. Before I explain why, let's get some food.

- What is technical debt? When we write software, we preferably want it to have the perfect design, have 100% code coverage, use all the latest and greatest tools and libraries. The reality is that when you create an application, you often have a deadline. In order to meet the deadline, there are going to be some things that you won't be able to do perfectly. You're going to use shortcuts in some parts of your program, to have something that works, but you know that you're going to fix it at some point in the future. That is called technical debt.

- Technical debt is a good thing. Especially if you're working at a startup. It's too expensive and it takes too much time to design and develop the perfect product. You need to take shortcuts to deliver something fast, measure whether your customers actually like it and then improve it or remove it depending on the outcome. It also means that more or less any software has some sort of technical debt. There's always something to improve.

- Technical debt doesn't only appear at the start of your software development. Programming languages evolve and introduce new features that require you to change the code you wrote in the past. I mean, look at how Python has evolved over the last years. Libraries get outdated, are replaced by newer, better ones, and you'll need to update your code to stay up-to-date. Because if you don't at some point you'll run into compatibility issues. And in my experience, the older a piece of software becomes, the more this becomes a problem. Being aware of, and managing technical debt is crucial for your software's long term survival.

- The 3 main types of technical debt are: deliberate, accidental/outdated design, and bit rot.

- Deliberate technical debt. In many cases, the quick way is the right way (to avoid over-engineering), but at times the team will intentionally do something the “wrong” way because they need to quickly deliver product to the market.

- Accidental/outdated design tech debt. When designing software systems, try to to balance thinking ahead and future-proofing your designs with simplicity and quick delivery. But systems evolve and requirements change. You might come to the realize that your design is flawed, or that new functionality has become difficult and slow to implement. A good original design will often be easier to refactor incrementally, but sometimes you may have to bite the bullet and do a more significant refactor.

- Bit rot technical debt. A component or system slowly devolves into unnecessary complexity through lots of incremental changes, often exacerbated when worked upon by several people who might not fully understand the original design.

- So why are these AH shopping cart coins technical debt? In the past, if you needed a shopping cart you could just grab one. The problem was that people took these shopping carts home. Used them to store stuff in, as decoration, or for your kids to play with, or whatever. But these carts are expensive. They cost 100s of dollars a piece. So, they added a system where you needed to put in a coin (a euro, or actually a Dutch gulden in the first versions). And that worked. But... nowadays people are using physical money, coins, less and less. So what was the solution? AH introduced these plastic coins that you can get for free and then you can still get your cart. But this is really weird. The whole idea of putting in these coins is that is dissuaded people from taking the carts home. But if you can get those coins for free, then what's the use? In the end, these coins are a temporary solution that allows us to use these shopping carts, but it's kind of weird. To do it right, AH needs new shopping carts that for example block when it's out of range of the supermarket building. But that's expensive. But there is going to come a point, where they'll need to redesign the system. Because now, I expect people are starting to take these carts home again. That's why this is technical.

- In order to keep technical debt in check, you need to manage it. I'll share a few tips with you on how you can manage technical debt. But before we dive into that, let's get some food.

## How do you manage technical debt?

- Have a code review process into place to avoid bit rot. If you're in a team, make the whole team responsible for the quality of the code.

- Most important thing is to make technical debt explicit in your planning. For example, if you're using something like Trello to manage your backlog. Add any technical debt items there as well. Explicit is good, because then you don't forget about these things and you see them every time you plan a new sprint.

- Always reserve some room in your sprint for solving technical debt. That way you're spreading the work instead of suddenly having to spend an extraordinary amount of time on solving it, and this also often comes at a moment when it's really inconvenient. You can plan technical debt items explicitly, but you can also leave a bit more planning room in your sprint and ask your developers explicitly to leave code behind in a better state than they found it in (Robert Martin's Boy scout rule).

- Make sure you prioritize/order technical debt items and also note any dependencies between them. You might have a technical debt item to replace a database access layer, but by doing that you might also need to upgrade your database. Don't start working on technical debt items before you have a clear view of what the consequences are of solving it.

- Define metrics to make explicit how much technical debt you have. Code coverage can help establish how much untested code you still have. You can define a percentage of technical debt items vs regular backlog items and set an alert when that percentage reaches a threshold. Count the number of bugs/issues and make sure to keep that count manageable. IF you solve a bug, also add a test to make sure the bug is fixed. If it ever reoccurs in the future, your test will immediately point it out.
