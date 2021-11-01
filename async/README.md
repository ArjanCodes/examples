# Introduction

# Explain the example

# Threads

To understand threads, a bit of background about what a thread means is required. To understand what a thread is, we must first understand processes. A process is a program. A process has its own (virtual) memory, separate from other processes. A process has one or more threads. The operating system will fairly switch between each running process so that all processes have a fair opportunity to execute. Now, a thread is like a process with one key distinction, a thread shares memory with the other threads in the process. Therefore, with the power of threads, a single process (AKA program) can do multiple tasks concurrently with the same memory available.
In our example, we use threads to perform tasks that spend the majority of their time waiting on the network. Specifically, each thread in the example calls the function `fetchPokemon` which will spend most of its time waiting for the network request to finish. Therefore, our program becomes much more efficient by running each of these I/O requests concurrently because we can initiate each before any responses are received.
While threads are a powerful tool, there are difficulties to be wary of. The first that shared memory is notorious for being the source of race condition bugs. To avoid these bugs, mutual exclusion is used (i.e. locks). However, mutual exclusion can lead to performance penalties and deadlocks if the programmer is not careful. Therefore, avoiding shared data as much as possible is typically considered best practice. Lastly, it is important to be cognizant not to overuse threads. Just because something can be run concurrently on a separate thread does not mean that you will reap performance improvements for doing so. Furthermore, there is also a performance overhead when using threads because of the context switch that the operating system must perform. As the adage goes, do not optimize prematurely.

# Asyncio

In computer science, future, promise, delay, and deferred refer to constructs used for synchronizing program execution. They describe an object that acts as a proxy for a result that is initially unknown, usually because the computation of its value is not yet complete.

In JavaScript, these things are called Promises, in Python they're called Futures. Futures and Promises are not exactly the same (though they're often used interchangeably). A future is a read-only placeholder view of a variable, while a promise is a writable, single assignment container which sets the value of the future.

Futures and promises come from functional programming, to decouple a value (a future) from how it was computed (a promise). These terms were first used in the 70s in computer science papers. Barbara Liskov published research in the 80s about creating pipelines of promises to reduce latency. If you know about the SOLID principles (and you should, you can watch my video about it by clicking in the top right), the L stands for the Liskov substitution principle which in short states that you shouldn't change the contract defined in a superclass. That's the same Barbara.
