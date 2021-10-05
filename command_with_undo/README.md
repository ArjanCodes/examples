## About this video

In this video I'm going to talk about the Command design pattern. You can use it to represent commands and have control over when they're executed. I'm going to show you an example of how to use it to implement an undo/redo system.

This video is sponsored by Skillshare. (skillshare section)

## Explain the example (screencast)

We start with a basic Bank and Account class. The example creates a bank and adds some accounts to it. We also deposit and withdraw some money. At the moment, this code is pretty limited though. We have little control over when transactions are executed, what to do when a transaction fails, etc. We can use the Command design pattern to make this more flexible.

## The Command design pattern (talking head)

The Command design pattern is a behavioral design pattern that provides a way to encapsulate all knowledge about executing an operation into a single object. Here's a class diagram. I'm going to show you how to use it to implement an undo/redo system and making transactions more flexible overall, using a bank example. Banks are a great example of where the command pattern is useful, because bank transactions follow the command pattern pretty closely.

## Implement the command pattern

- Create the Transaction protocol which represents a command.
- Create a few example transactions (withdrawal, deposit, transfer)
- Create the BankController class that executes the transactions.
- Create a few examples

## The basics of undo and redo (talking head)

Explain undo and redo stack.

## Add undo and redo management to the BankController class

## Increasing robustness using rollback

Add a command batch. If one of the commands in the batch fails, the whole batch is rolled back.

## Final thoughts

So as you can see, the command pattern is quite powerful. You can use it like I did to model transactions. It's also commonly used in non-destructive editing programs (photo editors for example). A related idea that I didn't really talk about in this video is that instead of storing the state (i.e. the balance on each account), you can also store the transactions and define that as your ground truth. If you then need to know the balance, you compute it by applying the transactions. This makes a few things simpler such as undo/redo, but it also makes a few things more complicated, such as knowing what the balance is on an account after a transaction. I might do another video where I cover this more in depth.

Hope you enjoyed this video, thanks for watching, take care and see you next week.
