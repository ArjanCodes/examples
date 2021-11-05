# Introduction

# Explain the example

# Threads

The traditional model of dealing with asynchronous and parallel code is the thread model. When you run a program, this starts a so-called process. A process has its own slice of memory that it gets from the operating system that's separate from other processes. Within a process, you have one or more threads. The operation system has a scheduling system that determines which processes get how much CPU time to run and switches between them automatically. So what's the difference between threads and processes? Well, as opposed to processes, threads share their memory. This means that you can perform multiple tasks concurrently that use the same memory. Especially if those tasks involve waiting for files to be loaded, or waiting for network requests to receive a response, then using threads can be very efficient because you don't have to wait for the server on the network to reply to you, but you can do something else while you wait.

While threads are a powerful tool, there are difficulties to be aware of. The first that shared memory is notorious for being the source of race condition bugs. To avoid these bugs, mutual exclusion is used (i.e. locks). However, mutual exclusion can lead to performance penalties and deadlocks if the programmer is not careful. Therefore, avoiding shared data as much as possible is typically considered best practice. Lastly, it is important to be cognizant not to overuse threads. Just because something can be run concurrently on a separate thread does not mean that you will reap performance improvements for doing so. Furthermore, there is also a performance overhead when using threads because of the context switch that the operating system must perform. Don't optimize prematurely / apply the YAGNI (You Ain't Gonna Need It) principle.

# Asyncio

In computer science, future, promise, delay, and deferred refer to constructs used for synchronizing program execution. They describe an object that acts as a proxy for a result that is initially unknown, usually because the computation of its value is not yet complete.

In JavaScript, these things are called Promises, in Python they're called Futures. Futures and Promises are not exactly the same (though they're often used interchangeably). A future is a read-only placeholder view of a variable, while a promise is a writable, single assignment container which sets the value of the future.

Futures and promises come from functional programming, to decouple a value (a future) from how it was computed (a promise). These terms were first used in the 70s in computer science papers. Barbara Liskov published research in the 80s about creating pipelines of promises to reduce latency. If you know about the SOLID principles (and you should, you can watch my video about it by clicking in the top right), the L stands for the Liskov substitution principle which in short states that you shouldn't change the contract defined in a superclass. That's the same Barbara.

# Change the example to now use async functions (after1)

- Add sleep messages to simulate delays for each of the devices
- Make the service async (including running the programm, which for the moment, just waits for each message to finish)
- To run an async program, use asyncio.run()

# Taking advantage of asynchronous operations by adding paralellism (talking head)

# Change the example to add run_sequence, run_parallel (after2)

Now it's possible to first flush the toilet before you clean it, yay!
