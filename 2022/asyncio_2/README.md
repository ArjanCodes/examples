## Intro

Modern software regularly interacts with an API, a database, or a file. That means there's a lot of waiting, and you need to make sure that your software handles that efficiently. If you don't, your application is going to be much slower, and the more data you process, the more you interact with APIs, the worse this is going to get.

The way to fix this is to rely on concurrency. In Python, you use the asyncio package for that. I'll give you a brief overview of how that package works, but then I'd like to go a bit deeper and also show you how to turn a regular, blocking function into something you can run concurrently, which could make your program a lot more efficient. And you don't even have to modify the original function for this, it's really easy.

I'll also talk about how concurrency affects your software's design and architecture, so make sure to watch this video till the end. If you want to learn more about how to design a piece of software from scratch, I have a free guide for you. You can get it at arjancodes.com/designguide. It contains the 7 steps I take when I design new software, and hopefully it helps you avoid some of the mistakes I made in the past. Arjancodes.com/designguide, and the link is also in the description of this video.

## Concurrent vs Parallel computing & asyncio recap

You may have heard the terms concurrent and parallel computing before, but what's the difference? True parallel computing means that an application runs multiple tasks at the same time, where each task runs on a separate processing unit.

Concurrency means that an application is making progress on more than one task at the same time, but may switch between these tasks instead of actually running them in parallel. If an application works on tasks A and B, it doesn't have to finish A before starting B. It can do a little bit of A, then switch to doing a little bit of B, and back again A, and so on.

This answer on StackOverflow nicely illustrates the difference: "Concurrency is two lines of customers ordering from a single cashier (lines take turns ordering); Parallelism is two lines of customers ordering from two cashiers (each line gets its own cashier)" (see https://stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism). If you translate this back to computers, each cashier is a processing unit, a CPU core, each customer is a task that the processor needs to take care of.

Modern computers use a combination of parallelism and concurrency. Your CPU might have 2, 4, 8, or more cores that can perform tasks in parallel. You OS will run 10s to 100s of different tasks concurrently. A subset of these tasks are actually running in parallel while the OS seemlessly switches between the tasks.

Parallelism in Python has a caveat, which is the Global Interpreter Lock. Any time you run Python code, it needs to acquire an interpreter lock. There are reasons for this that I won't go into in this video, but it effectively means that Python code is single-threaded, even if you start multiple threads. There are ways around this, for example by relying on multiple processes instead of multiple threads, or by switching to an interpreter that doesn't have the lock. Note, this concerns parallelism. Concurrency on the other hand, works really well in Python, especially since version 3.10.

Why is concurrency a smart way to do computing? Well, it so happens that many tasks involve waiting. Our applications are waiting for files to be read or written to, they're constantly communicating with other services over the Internet, or, they're waiting for you to input your password or click a few buttons to help identify traffic lights in a recaptcha (I hate those things).

It considerably speeds up things if a computer can do something else while waiting for that network response or for you to finish cursing about recaptchas. In other words, concurrency is a crucial mechanism for making our computers work efficiently in this age of connectivity.

The asyncio package in Python gives you the tools to control how concurrency is handled within your application. As I've talked about in my previous video, the async and await syntax is the mechanism to achieve this. If you write async in front of a method or function, you indicate that it's allowed to run this method or function concurrently. Await gives you control over the order that things are being executed in. If you write await in front of a concurrent statement, this means that the portion written below that statement can only be executed after the concurrent statement has completed.

Being able to do this is important, when the next part of your code relies on the result of the previous part. This is often the case: you need to wait until you get the data back from the database. You need the data from a network request in order to continue, and so on.

## Recap of async

- Show async and await syntax (using the asyncio_recap example without explaining http_get but simply using it)
- Show gather to run multiple http requests concurrently (asyncio_gather for an example and time difference)

## Turning non-async code into async code

- First show the wrong way of trying to do it (i.e. create a task, then do the request, then await the task to complete)

- Show the to_thread method from asyncio. This creates a separate thread that will run concurrently with other threads (or the OS may decide to run threads in parallel on separate CPUs).

- Show the simple req_http module that allows for async requests.

- Mention aiohttp as an alternative (show req_http_aio)

- The to_thread function from asyncio creates a thread to run a blocking function in, and then integrates it with the event loop.

## Design patterns

How does async change the way design patterns work? In principle, not at all. Due to the clean await/async syntax, there's not effect of coupling or cohesion by introducing asynchronous code in your application. For example, if you want to use the Strategy pattern, you can create an asynchronous method in your Strategy class and then call that. If you want to use the Factory asynchronously, no problem: create objects asynchronously if you want to. The basic pattern doesn't change. Just parts of the pattern become awaitable.

On the architectural level, async programming might have some impact depending on what you do. You can imagine that if you're processing data in a pipeline that relies on asynchronous operations (which is quite common), you'd want to adapt the data structure so it allows you to specify what to run concurrently, vs what to run in sequence. I gave an example of this in my previous video where I showed how you can create a nested structure of sequential and concurrent function calls. If you'd like me to go into more detail on this in another video, let me know in the comments below.

## Final thoughts

As you can see, there are lots of ways you can use asynchronous code in Python to write more efficient programs. Hope you enjoyed this video. If you did, give it a like and consider subscribing to my channel if you want to learn more about software design and development.
