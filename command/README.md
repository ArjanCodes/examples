## About this video

In this video I'm going to talk about the Command design pattern. You can use it to represent commands and have control over when they're executed. I'm going to show you an example of how to use it to implement an undo/redo system.

This video is sponsored by Skillshare. (skillshare section)

## Explain the example (screencast)

We start with a basic Bank and Account class. The example creates a bank and adds some accounts to it.

## The Command design pattern (talking head)

The Command design pattern is a behavioral design pattern that provides a way to encapsulate all knowledge about executing an operation into a single object. Here's a class diagram. I'm going to show you how to use it to implement an undo/redo system, using a bank example. Banks are a great example of where the command pattern is useful, because bank transactions follow the command pattern pretty closely.

## Implement the command pattern

- Create the Transaction protocol which represents a command.
- Create a few example transactions (withdrawal, deposit, transfer)
- Create the BankController class that executes the transactions.
- Create a few examples

## The basics of undo and redo (talking head)

Explain undo and redo stack.

## Add undo and redo management to the BankController class
