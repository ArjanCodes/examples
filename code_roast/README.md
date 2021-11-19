# Introduction

(start with screencast). There's something very interesting in this code (show the main() function only). What do you think will happen if I print the class name of FileRequest: "print(file_request.**class**.**name**)? It should print "FileRequest", right? Well, let's see... Ooohhhh... that's interesting. The FileRequest initializer doesn't create a FileRequest. I love code that changes the meaning of core Python concepts. We're gonna have some fun untangling this mess. Let's dive in!

# Thanks (talking head)

In this code roast episode, I'm going to analyse and refactor a pdf and web scraping script that analyses academic papers. Thanks to John Fallot for supplying the code for this roast, let's first walk through the code to see how everything is setup, and then I'll do an analysis and start refactoring. I'll be using Tabnine, who's the sponsor of this video.

# Tabnine sponsored section

# Explain the example and analysis (screencast)

Analysis:

- This code changes the what basic programming concepts like class initializers do. Really bad idea! Look at the ScrapeRequest class: the superclass creates subclasses for you based on a parameter that you pass to its initializer??? You're redefining what a class initializer should do. And introduce a lot of coupling at the same time, because the superclass needs to know all its possible subclasses. I'm going to give you three reasons why this is a VERY BAD IDEA (tm) (add title over this). But first let's look at the rest of the code.

It's not even clear what problem this is supposed to solve, because in the main function, you know what you want to do, so why not simply create the class that you need there? If you really want to create the class dynamically, based on a string value that you read from a file, use the Abstract Factory pattern instead or even simpler: maintain a dictionary that maps strings to class initializers. Naming is not precise. The function is called 'download', but it actually is not downloading in all cases (e.g. not in the case of PDFScrape, which surprisingly isn't a subclass of ScrapeRequest - why the special case?).

- The FileRequest hierarchy is really convoluted and not necessary since each class basically contains a single function. It also does the same weird thing as ScrapeRequest. Naming is also not very precise. For example, not all subclasses deal with files. DOIRequest gets a data frame, analyzes it and return another dataframe. The FolderRequest actually specifically deals with PDF files. The fact that they're in a folder is not that interesting.
- If you look at the code of a single class, like the PDFScrape class, lots of information is stored as instance variables, where they should actually be local variables in the method. Also, data like research words is hardcoded in the methods, which is a bad idea.
- There's code duplication in the logging system: because you send it to a log file and print it to the screen and didn't write a separate function for this, you now create a variable to store the message in, and then still have the duplicate code.
- Having lots of comments, thank you messages, etc at the top of the code file is a bad idea, because you almost never look at that text as a developer and you constantly need to scroll past it when you edit the code. It's better to put this in a separate readme file.
- Configuration settings are a bit all over the place. Some things are defined at the top, others locally in the main file (like where the papers are located).

# Talking head

Several reasons why changing the meaning of basic programming concepts is a REALLY BAD IDEA:

1. You need a lot of boilerplate code with low-level dunder methods to do this, which makes your code really hard to understand
2. Anyone who uses your package is going to work from a set of basic assumptions of how things work in Python. If you change that, your package becomes hard to use because it does unexpected things.
3. Because the basic rules no longer apply, lots of things are going to break your code if you want to change the design. Add another subclass? Doesn't work, you need to dive into the low-level code in the superclass to fix it. Want to add type hints? Too bad, since you have to rely on a generic keyword arguments object because it's dealt with in ScrapeRequest. Forgot what the slookup boolean meant or the dlookup string? Too bad, you'll have to dive into the low-level code again to find out.

So in short, whenever you feel that you need to change the core of how a programming concept works to get the job done, consider very carefully whether that's really needed. AND THEN DON'T DO IT!!! I've been developing software for more than 25 years, and I've never encountered a situation that I could only solve by changing the meaning of a programming concept. There are better solutions, it leads to a big mess. DON'T DO IT.

Refactoring PART 1:

- Create a scraper package with **init**.py
- Move PDFScraper to another file, fix the imports
- Create a separate function called fetch_terms_from_pdf_files in fetch.py containing what was in FolderRequest
- Delete FolderRequest from main as it's no longer needed.
- Change DOIRequest and PubIDRequest to functions as well and put them together in fetch.py.
- Simplify PDFScraper by removing all the instance variables and let the data use files (hardcoded in the class for now, will improve config in the next part)

In the next part, I'm going to cleanup the scraper code and use a better mechanism for dealing with configuration settings. Thanks again to the sponsor, Tabnine - check them out via one of the links in the description. If you enjoyed this video, give it a like, this really helps promote my channel on YouTube, and subscribe if you enjoy my content. If you want to watch another data science code refactoring like this, check out this video. Thanks for watching, take care and see you next time!

---

# Code roast part II

## Introduction (talking head)

In last week's video I started refactoring a pdf and web scraping script. If you haven't watched that video, I recommend you watch that one before continuing. I've put the link in the description.

I'm not a data scientist myself, I'm a software engineer. So I view data science projects like this through the lens of a software engineer or designer. If you want to learn more about data science itself, Skillshare, this video's sponsor, has lots of great classes to help you get started.

## Skillshare sponsored section

## Recap the example (screencast)

## What I'll do in Part 2 (talking head)

In this part of the refactoring, I'm going to clean up the scraper classes, move a few more things to different files and then show you how to properly deal with the configuration settings for this project.

## Refactoring PART 2 (screencast)

- Create a Scraper protocol class and let the other scrapers inherit from it
- Move the other scraping classes to a separate file.
- Move change_dir and export to separate files and pass config settings (such as the export dir) as an argument
- Improve logging
- Separate config into a JSON file and use a dataclass. There are way more possibilities with a package like Hydra, but I'll cover that in a future video.
- Put the words separately in a text file.

## Final thoughts (talking head)

Thanks again to John Fallot for supplying the code. I know I was a bit more roasty in this video, especially about the scraper initializer. But you, sometimes a bit of tough love doesn't hurt. In the end, I want you to become better at this stuff, as that's what my channel is all about. I've written down a guide to help you get started. You can get it for free by going to arjancodes.com/designguide. It describes the 7 steps I go through when I design my software. It's short and to the point, really actionable stuff that you can apply right away to your own projects. So, arjancodes.com/designguide for your free download.

I do hope you enjoyed the video, and if you did, give it a like and consider subscribing to my channel if you're not a subscriber yet. If you're a subscriber already, why not unsubscribe and then subscribe again, to enjoy the awesomeness that is the YouTube subscribe button. Thanks for watching, take care and see you next week!
