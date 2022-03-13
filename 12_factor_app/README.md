If you want to build a scalable software-as-a-service product, that's easy to maintain, you need to set it up in a very specific way. Doing that is really important, because if you don't, you're going to run into a lot of problems, your software won't work well, your customers are going be unhappy, and ultimately your product is going to fail.

I'm going to share 7 things you can do to avoid that. It's based on my own experience developing cloud services for my company, but I've also taken inspiration from something called the 12 Factor App, that I'll talk about in a minute.

This video's not Python-specific by the way and it's not really about software design either. But that doesn't mean software design doesn't play a role here. Thinking carefully about software design is going to help you choose the right technologies that will best serve your product. I've written a guide to help you with designing new software from scratch. You can get it for free at arjancodes.com/designguide. It's based on my own experience developing at least three different software-as-a-service products over the last five years. You know, why not benefit from my experience to avoid some of the mistakes that I made in the past? If you go to the link below and enter your email address, you'll get it in your inbox right away.

Back in the day, if you bought software, you got a bunch of floppies, a CD-ROM, or a DVD. I remember buying WordPerfect 5.1 on 12 floppies. And then when you're installing it and you're at floppy 10 out 12, of course then that disk is damaged. Ah, the memories. When the Internet took off, companies switched from sending you physical disks to allowing to download the software instead. And now that cloud technology is maturing, we're no longer directly downloading software, but software is delivered as a service instead.

Because the way software is delivered has changed so much, the way we design, develop, and deploy it has also changed. Except for products that heavily rely on integrated hardware and software, like cameras, digital pianos, or cars, but even there you see it's become a standard to have semi-regular firmware upgrades.

So how do you setup a "modern" software as a service product? There's a methodology called the 12 Factor App that describes the best practices for this. It's already quite old - it dates from 2011 - and it was written by the developers of Heroku, a well-known cloud provider. And in fact, most of the cloud providers you see today (AWS, Azure, Google Cloud) are all built on the principles of the twelve-factor app.

I don't want to go through each of the twelve factors in this video, because some of the factors are more relevant than others, but I want to go through seven of them and give you my take on them. And as a bonus, I'll share a few personal tips for making software releases less stressful. So, let's dive in.

# 1. Codebase: One codebase tracked in revision control, many deploys

The first factor states that you should store the code in a version control system like Git. There should be a one-to-one correlation between your codebase and the app. So if your app is a website, the code that renders that website should be in a single repository. It's possible that your app consists of multiple services: your website (or frontend) server, a backend server, a database server, services for specific things like handling payments, performing analytics, etc. Each of these should be defined in a separate repository, at least the ones you're developing yourself. More about that later.

If your apps and services need to share code (like certain data structures or interfaces), extract these into libraries that you can then include using a dependency manager. If you're building a service with JavaScript or Typescript and Node.js, you can use npm. In Python, you can use Pip, or more advanced tools for managing dependencies like Poetry.

There is one codebase, but there can be multiple deploys. A deploy is a running instance of your app. The production version of your app is one of the deploys, but there can be other versions running as well: a version locally on your machine, a version used for testing, a staging version, and so on.

# 2. Dependencies: Explicitly declare and isolate dependencies

In most programming languages, you have a mechanism for handling the dependencies that your application needs. If you're doing Typescript or JavaScript development, then you'll probably use NPM or Yarn. Rust has the Cargo package manager. In Python, that's Pip. A 12 factor app doesn't rely on system-wide installed packages, but it declares all its dependencies using some kind of manifest file. In Typescript and JavaScript, this is the package.json file that contains all the dependencies. If you're using Pip in Python, this is the requirements text file. Because there's only a single codebase that's deployed one or more times to different environments, the specification of these dependencies is also the same for both production and development environments. Though of course, these can be attached to different branches in your Git repository.

A second thing that's important for dealing with dependencies is that there's also a way to isolate dependencies so to ensure that you're not accidentally using dependencies from the surrounding system. In Python, you can use something like virtualenv to isolate your dependencies. If you want to take this a step further, there are overarching dependency management and isolation systems like Poetry (I'll put a link in the description).

But even then, there's another layer of isolation that you can benefit from, and that's the system-wide specification of dependencies and providing an isolated execution environment. The tool for this that everyone uses is obviously Docker. This is a virtualization layer that allows you to specify exactly which operating system and version you'll be using, and install any extra dependencies that you need as well. The Dockerfile is the manifest specifying the execution context and can install dependencies that you need. Docker containers are the virtual machines that provide the isolation.

# 3. Config: Store config in the environment

Depending on the deploy of your app, you're going to have many configuration settings. These settings will be different for the different deploys. For example, you production web application will be on a different domain that your staging or development version of the app. And there are other things that might be different:

- Connecting to the development database in stead of the production database
- Credentials for storage locations like Amazon S3 or Google Cloud storage
- Credentials of other services like email clients or other third-party integrations
- You may even have globally enabled or disabled areas of your application depending on the deploy. For example, an admin area might not be visible by default in production, you could have features that you're already building but they're hidden behind a global feature flag, a global maintenance mode that is on or off, logging settings, and so on.

These kinds of settings shouldn't be part of your codebase. If you're for example storing these things as constants in the code, this is a violation of the 12-factor app. A good test to verify that you're setting up configuration correctly is whether your code could be released as open source without giving public access to any credentials. Another test is to verify that if you give access to your repository to let's say an intern, that you can control what the intern has access to. This is especially important because everyone at a software company always makes jokes about interns. If you piss them off too much, they might be out for revenge and you don't want them to have access to the production database at that point, do you?

The most common place to store these settings is by using environment variables. They're language and OS agnostic. Most cloud providers offer the possibility to define environment variables as part of your virtual server. For example, if you launch a Google Cloud function, you can add environment variables which are then available to the app at startup.

You can also use a tool like dotenv to group your variables into a single dot env file. This works well for local development. Whenever a new developer wants to start working on the code, you can provide that developer a dot env file containing all the necessary credentials. But you have to make sure that you don't accidentally commit the .env file to your repository.

For some configuration settings it might make sense to make them part of the code. For example the names of the routes in a web app, file size limits for uploads, default prefixes for database ids, etc. These things are probably not going to be different for different deploys, so you can keep them in the code itself. As soon as they change depending on the deploy though, move them out into environment variables.

# 4. Strictly separate build and run stages

Deployment of your code should happen in three independent stages: build, release and run. In the build stage you convert your code into an executable bundle. It contains any dependencies and other assets that the code needs. If you use Docker, this would be the Docker image.

You then have a release stage that combines any configuration settings with the build output. If you're using something like Kubernetes this is the definition of a deployment that links a Docker image with other settings like environment variables, information about the number of replicas and so on.

Finally, there's the run stage that actually loads the Docker image and starts the service according to the release configuration.

Every release should have a unique id: can be a timestamp, or a version number. Once you create a release, it can't be mutated. Any change must create a new release.

Separating build, release and run stages means for example that you shouldn't change code in a service that's currently running. You should change it in your code base, then build, release and run a new version.

You can initiate a build and release when you're changing code. For example, we have coupled this with pushing our code to a develop, staging and production branch which automatically launches a build. You can do this really easily with GitHub Actions nowadays. If you're not using GitHub but for example BitBucket, they also have a similar feature called Pipelines.

Kubernetes is a good example of a system that manages the run stage. If a service crashes, it's automatically restarted. Or if a service starts to be overloaded by requests, Kubernetes can scale it up automatically.

# 5. Processes: Execute the app as one or more stateless processes

It's really important to make a distinction between what parts of your system maintain state and which parts don't. Examples of things that maintain state are your database, a cache, file storage, etc. Anything else shouldn't maintain state. So for example if you develop an API service that acts as a layer on top of your database, it shouldn't have any state. You might be tempted to do things locally, like maintain a log file, or store user activity. Don't. Because if you ever decide to scale up and maintain multiple services in parallel, this can result in a big mess.

Twelve-factor processes are stateless and share-nothing. Any data that needs to persist must be stored in a stateful backing service, typically a database.

You may use space temporarily if that's part of the transaction, but basically any request that an API handles should be isolated and not rely on data obtained in a previous request. For example, at my company we have a server that runs code on demand based on a set of files from a git repository. So when we handle each code running request, we retrieve the files from the Git repository and store them in a temporary folder, run the code and then delete the files again.

Basically, you should assume that at any moment, your stateless service could be restarted and any local data will be lost.

# 6. Maximize robustness with fast startup and graceful shutdown

If you look at applications running in the cloud, they generally rely on processes that can be started and shut down at any given moment. That's why it's so important to make sure that you clearly separate stateful and stateless parts of your application. If many of these processes are disposable, it means it's easier to deploy changes, and scale up or down your services to meet demand.

Make sure that your processes can be started quickly. This means you need to be careful with services that rely on first loading lots of data remotely or where starting the service relies on complex computations like training a machine learning model first before deploying the service that allows access to that model. You can solve this by making sure the data that a service needs is close to the service (i.e. available in the local file system), or if you rely on complex computations, introduce a stateful component like a cache so your service can be up and running quickly using cached computation outcomes, and recompute parts when needed (for example, if there's a change in configuration).

Also make sure to take care of cleanup when your service shuts down. This can be things like closing the database connection (this is important, because too many open connections can slow down your database), and making sure any local data is synced with stateful resources like a cache or cloud file storage.

The twelve-factor app’s processes are disposable, meaning they can be started or stopped at a moment’s notice. This facilitates fast elastic scaling, rapid deployment of code or config changes, and robustness of production deploys.

# 7. Keep development, staging, and production as similar as possible

One thing that has really saved us a lot of time at my company is making sure that the various environments you deploy to are as similar as possible. And nowadays, we have lots of tools available to help us achieve that. Docker not only allows you to package up your application and its dependencies into a single isolated image, you can also run that image on your local development machine. That way the locally running system will be much closer to when you deploy it. You should still have at least a staging environment though where you check that things also work as expected with a copy of the production data.

# Three additional tips to make releases easier

1. Do many small releases: releases have to become boring
   1. Use feature flags to switch off parts of your code that are not yet ready to be used
   2. Use testing to guarantee stability
   3. Unleashing a new feature onto your customers doesn’t have to coincide with a code release. Make it a flag you can switch on or off.
2. Don’t try to make small improvements right before a release
3. You don’t have to be up-to-date with the latest-and-greatest

Link: https://12factor.net
