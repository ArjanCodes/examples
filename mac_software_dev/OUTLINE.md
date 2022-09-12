# Is a Mac good for software development?

Is a Mac a good machine for software development? There's a few areas where I think the Mac is hard to beat. But in some other areas, you should avoid it. I'm going to talk about the pros and cons of using a Mac for software development. And then I'll make a few recommendations for which Mac to buy and what you should pay attention to.

This is the machine I use, a 16" M1 Max MacBook Pro. This is actually not the best option for software development, but I'll share later on why I still bought this.

## Operating systems

Let's talk about operating systems

It all comes down to personal preference and the type of work you do.
First, don't forget Linux. The vast majority of the Internet runs on Linux servers, for a lot of reasons:
It's free - no point in paying a license fee for each server in a huge data center
It's open-source, so you can customize everything
It's designed to be fully operated by the command-line if you want - either locally or remotely. That works really well for managing a large fleet of servers.
Programmers who work on a lot of back-end web server code often like macOS for their personal computer, because it's based on Unix and easily runs nearly all Linux software - combined with the fact that Apple makes great hardware, and everyday things like watching a video work a little easier on macOS than on Linux.

However, Windows also has a lot of other advantages. If you're programming for the enterprise, Windows is still the king. Visual Studio is an amazingly good IDE, and the whole Microsoft development stack is fantastic. There are some amazing third-party tools for graphics, debugging, profiling, and so many other things - they do tend to be proprietary and expensive, but on the other hand they tend to be very clean, robust, well-documented, and easy-to-use

The Windows Subsystem for Linux and the recently added SSH on Windows add a lot of Linux functionality.
Systems like Docker are obfuscating the Linux environment. Sure, many docker images are still based on Linux, but you can develop and deploy an application without ever being aware of it.
.NET Core supporting Linux is further blurring the lines.
You can easily use Visual Studio to write C#, build a Linux docker container, and deploy it without ever needing to touch Linux in any real way.

Shwo usage in StackOverflow survey: https://survey.stackoverflow.co/2022/#methodology

## Reasons why a Mac is good for software development

### 1. The OS is based on Unix

As a back-end dev, I always ask for a Linux laptop if it's available and a Windows laptop if not - MacOS is bsd rather than gnu, which means that shell scripts will usually run on both but will often give inconsistent results. For example, take curl - writing a curl on a Mac and then copying it to a Linux shell often fails in more complex use cases, particularly where mpf data is concerned. The base64, tr, and wc utilities don't even have all the same -options and base64 behaves differently by default. By contrast, I can use cygwin or wsl on Windows and get gnu-compliant utilities that don't collide with what comes installed with the OS.

Long story short, macOS is built on top of Darwin, which is built around BSD, which is based on Unix and is also POSIX-compliant. For this reason, macOS is also POSIX-compliant and therefore can handle ports of most Linux software. Homebrew does this. It’s amazing.

Being Unix-based has some advantages. While Windows has mostly GUI tools with simple interfaces, macOS allows you to dive deeper with the terminal and use real shells like bash, fish, and zsh. Windows can do this to some extent with WSL, but it will never offer the same experience macOS does with its inferior GUI-centric infrastructure.

Homebrew is a full package manager for macOS that works just like you’d expect. MacPorts is less so a drop-in replacement, and more so a repository of direct ports of Linux tools. iTerm2 is an amazing terminal that works much better than the default one provided by the OS.

### 2. Gestures & keyboard shortcuts

MacOS has really useful gestures and keyboard shortcuts. All the different keyboard shortcuts make software development (which is keyboard-focused) a breeze. Spotlight is really great to quickly find stuff and launch apps.

Window management on macOS is lacking. But you can use a free tool called Rectangle to fix that.

### 3. Battery life

IF you're working on one of the laptops, you'll have great battery life.

### 4. iOS development & web development

You need a Mac for iOS development. For doing web development, it's useful to have easy access to Safari (which needs to be tested because it doesn't use Chromium under the hood).

Also: macOS has hovering scrollbars. Very minor, but I never liked Windows’ scrollbars, which cut into the content. macOS has scrollbars that hover above the content, disappearing when not in use.

### 5. macOS stays out of your way so you can get shit done.

One of my friends has a saying. It goes like this:

“Anyone can buy a Windows machine and do whatever they want with it, but when you see someone with a Mac, they really mean business. You don’t just buy a Mac because they’re pretty. You buy a Mac to get shit done.”

macOS has a huge getting-shit-done factor. While the newer laptops are arguably very lacking in hardware (and function keys, fuck you Apple), the software is still spot-on.

Anyone who knows what they’re doing will spend hours upon hours configuring Windows. Removing spyware, disabling telemetry, uninstalling bloatware, and suppressing tracking. And that’s just removing things.

Anyone who doesn’t know what they’re doing will spend a day every few weeks reinstalling Windows because it gets that bad. Yes, that happened to me. I learned the reinstalling Windows dance when I was 8 years old (possibly even earlier). I could give you a step-by-step walkthrough about how to use the installer without once looking at any documentation.

## Sponsored section (SANDMARC)

Before I dive into the reasons why you shouldn't buy a Mac for software development, I want to show you some of these Apple accessories that Sandmarc sent to me. They have a collection of really nice sleeves and cases, full-grain leather and it feels really premium. Like this carrying case for the MacBook Pro. Or here I have a really nice band for the Apple Watch. It feels comfortable. I also have the AirPods case here. And they have more. It's all part of their leather collection that comes in either Black or Brown colors Thanks Sandmarc for sponsoring this section of the video - check them out via the link in the description.

## Reasons why you shouldn't use a mac for software development

### 1. Developing games

Lots of games are Windows-only. In the pas Mac was the only machine where you could run Linux, Windows and MacOS. With Apple Silicon it's no longer the case.

### 2. New Apple Silicon

The new Apple Silicon is great in terms of power efficiency and speed. It also means that some software doesn't work perfectly yet or have caveats, like Docker. By default Docker Desktop (for apple silicon) will pull down arm64 images. However, you can specify the platform via a command line prompt or docker-compose.yml (ie (--platform=linux/amd64) . You can use mixed platforms simultaneously, docker will either emulate arm or virtualize x86 as necessary. If you're not careful, you might create a Docker image locally using arm64 and then try to run it in the cloud in Linux and it won't start. I know, because that actually happened to me.

## 3. Peripherals (mainly an issue with M1)

Users can connect just one additional monitor with the M1 MAcBook Air and Pro. This is not an issue on the M1 Pro/Max laptops. The M1 Mac Mini can connect up to two monitors. Though there are some workarounds using DisplayLink adapters and the USB-C port.

### 4. Pricing

Depending on the machine you get, it can be very expensive and you'll be paying for lots of stuff that's not important purely for software development:

- Screen quality on laptops is great, but you'll probably use an external monitor anyway for coding
- You're paying for media exporters that are built into the chip. If you're doing video editing, that's useful. For coding not so much.
- You're paying for SD card readers, HDMI output, really good speakers on the laptops. All of this is not that important for software development.

### 5. Configurability

You have a limited number of possible chip configurations. If you like customizing your machine, you're not going to be happy with a Mac. There's no way to upgrade things like RAM or harddrive later on. What you buy is what you get. Well, unless you buy the uber-uber expensive Mac Pro.

You have to make sure that when you buy the machine, it's future-proof so you don't have to replace it within a few years. And then you pay Apple's prices for RAM and SSD storage.

### 6. BONUS: pedantic issues

- OS X creates dozens of hidden files like .DS_Store which can really be annoying if you work a lot with file processing.
- To this date - can’t open an archive file. Instead, OS X insists on extracting it.
- Window management. Ugh

## What mac should you buy as a developer?

- Machines that are a great option for software development are:
  - M1 MacBook Air (a truly great laptop and great value at the price). M1 works great for software development (I've been using one for the past year to do pretty intense backend and web development)
  - If you just need a desktop: M1 mini has the same performance or even a bit better than the M1 Macbook Air due to the fan and it's pretty cheap.
  - If you need a bit more performance: M1 MacbookPro 14. It's more expensive, but it's also a way faster machine with the M1 Pro
- What you definitely shouldn't buy:
  - M1 Max (same CPU performance as the M1 Pro)
  - M2 Macbook Air (it's a bit more performant than the M1 - but if you need performance and want a Mac, you should go for the 14" pro IMO) - too expensive for what you get

In terms of specs:

- What you buy is non-upgradable, so make sure you know what you need before.
- RAM: 8GB does the job, but it's shared, so personally I opted for 16GB. Especially if you want to run Docker containers locally, you'll be glad you went with 16GB.
- Storage: 256GB is okay, but since the hardware is not replacable, only get this version if you're really, really sure you don't need the space. Personally, I recommend going for 512GB at least. If you're doing web development, that node_modules folder can get pretty large pretty quickly. Docker images can also be quite large, so be aware.

Hope this video gave you some insight into whether you should buy a Mac for software development, and which one. If you want to learn more about my Mac setup and the apps I use - there's a few you definitely should know exist, check out this video next.
