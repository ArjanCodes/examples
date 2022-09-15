# Is a Mac good for software development?

Is a Mac a good machine for software development? There's a few areas where I think the Mac is hard to beat. But in some other areas, you should avoid it. I'm going to talk about the pros and cons of using a Mac for software development. And then I'll make a few recommendations for which Mac to buy and what you should pay attention to.

This is the machine I use, a 16" M1 Max MacBook Pro. This is actually not the best option for software development, but I'll share later on why I still bought this.

## Other operating systems

Let's first talk about the other two main operating systems: Linux and Windows. Which OS you use for a large part comes down to personal preference.

The majority of services on the Internet run on Linux server, for a lot of reasons:

- It's free, there's no point in paying a license fee for each server in a huge data center
- With tooling like Docker, the images running in the cloud are mostly running some version of Linux.
- Linux is designed to be operated by the command line: locally or remotely. Works well if you have to manage lots of servers.

Windows has other advantages. If you're programming enterprise applications, it's a great option with C#, .NET and the surrounding ecosystem. Visual Studio is great IDE. Though nowadays Visual Studio Code is a lot more popular than Visual Studio. More than twice as many people use it (show StackOverflow overlay).

Then you have Windows Subsystem for Linux. I haven't used this personally, but of course this adds a lot of Linux functionality to Windows.

So, is there a winner? Well, if you look at the StackOverflow survey, you see that almost half of the software developers use Windows, about 40% use Linux, and about a third use macOS. Those percentages add up to more than 100%, but of course lots of developers use multiple OSes in their work.

Show usage in StackOverflow survey: https://survey.stackoverflow.co/2022/#methodology

## Reasons why a Mac is good for software development

### 1. The OS is UNIX-compliant

If you're doing a lot of backend development, macOS is actually a nice option. macOS is a UNIX 03-compliant operating system. macOS is also POSIX-compliant and therefore can handle ports of most Linux software. This is what the really awesome Homebrew package manager does.

You also have nice apps such as iTerm2 terminal that works much better than the default one in macOS.

The hardware is generally good, except for a turds in the past like the 12 inch MacBook or the overheating Intel MacBook Pros. Also the OS is really well optimized for user-friendliness and creative workflows so doing your everyday work, or things like watching a movie or listening to music on a Mac is very pleasant.

### 2. Gestures & keyboard shortcuts

MacOS has really useful gestures and keyboard shortcuts. All the different keyboard shortcuts make software development (which is keyboard-focused) a breeze. I'm still regularly learning new keyboard shortcuts, so I'm quite far from being a complete keyboard wizard. I'm more of a keyboard hobbit I guess.

Another really great builtin tool is Spotlight. You can use this to quickly find stuff and launch apps.

Window management on macOS is lacking. Not just lacking, it's pretty bad. But you can use a free tool called Rectangle to fix it.

### 3. Battery life

If you're working on one of the Apple silicon based laptops, you'll have the best battery life in the industry. This is really handy if you're working remote and you don't have access to electricity. Apple's modern laptops will get you through the day comfortably.

### 4. iOS development & web development

You need a Mac for iOS development, unless you don't want your app to appear in the App Store for some reason. If you're doing web development, it's useful to have easy access to Safari. You need to test things on Safari. It doesn't use Chromium under the hood, so you will run into issues.

For example, a big difference is that macOS has hovering scrollbars. It's nice because the content can use a larger portion of the screen real estate. But it might break your web app's layout. And there are a bunch of smaller incompatibilities, especially on mobile where the visible section of the content resizes if you scroll down because the address bar disappears.

### 5. macOS stays out of your way

For me, if I buy a new Mac machine, getting things ready for work is really easy. I don't need to install a bunch of drivers, uninstall lots of bloatware, copying over settings from the previous machine.

I don't want to do all that stuff. I use my Mac for my business. So it needs to just work. I haven't used Windows for a while, so things have probably improved on that end as well, but a Mac simply feels effortless to me to get going quickly. Time is money.

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

You have a limited number of possible chip configurations. If you like customizing your machine, you're not going to be happy with a Mac. There's no way to upgrade things like RAM or harddrive later on. What you buy is what you get. Well, unless you buy the uber-uber expensive Mac Pro which is totally overkill for most software developers. And at the time of publishing this video, that still runs on Intel and is actually beaten in some tasks by the newer, and much cheaper Apple silicon Macs.

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
  - M1 Max (same CPU performance as the M1 Pro). The reason I got this is because I do a lot of video editing. And the M1 Max has more powerful encoding and decoding chips. The SD Card reader is really use because all my cameras record on SD Cards. And I like the bigger screen because then I don't need a monitor at home when I'm editing videos (though 16" is not the same as working on a 24 of 27" monitor, it gets the job done)
  - M2 Macbook Air (it's a bit more performant than the M1 - but if you need performance and want a Mac, you should go for the 14" pro IMO) - too expensive for what you get

In terms of specs:

- What you buy is non-upgradable, so make sure you know what you need before.
- RAM: 8GB does the job, but it's shared, so personally I opted for 16GB. Especially if you want to run Docker containers locally, you'll be glad you went with 16GB.
- Storage: 256GB is okay, but since the hardware is not replacable, only get this version if you're really, really sure you don't need the space. Personally, I recommend going for 512GB at least. If you're doing web development, that node_modules folder can get pretty large pretty quickly. Docker images can also be quite large, so be aware.

Hope this video gave you some insight into whether you should buy a Mac for software development, and which one. If you want to learn more about my Mac setup and the apps I use - there's a few you definitely should know exist, check out this video next.
