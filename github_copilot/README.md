## About this video

This video is about GitHub Copilot. I'll basically be monkeying around with the tool and see how it works and discuss my thoughts about it.

## Video outline

### What is Github Copilot?

Last month, Github introduced Copilot. They call it an AI pair programmer that helps you write code faster and with less work. I like that. Because I'm a lazy bastard. Today I'm going to put it through its paces and see if it delivers what they promise. In short: I'm impressed. But I'm concerned about a few things. Let's dive in.

-- teaser of me being flabbergasted that something works

If you're new here and you want to become a better software developer, gain a deeper understanding of programming in general, start now by subscribing and hitting the bell, so you don't miss anything.

### Installing it in VSCode

Copilot integrates directly with VSCode. You can install it as an extension. At the moment, you need to be in the Technical Preview group in order to use it. I put a link in the description that you can click on if you want to join the waitlist.

### Play around with the tool

Using it is pretty straightforward. It automatically suggests code snippets. You can use Command or Ctrl + square brackets to see the options you can choose from. If you want to use a snippet, press Tab and it's added to your code. If you don't want any of the suggestions, press Enter, or just keep typing.

The interface integrates well with VSCode. Really basic. Does the job and doesn't get in the way. You can see that they thought about this.

- Try a few basic functions:

  - Basic Copilot example to compute date difference
  - Exponential moving average
  - Read settings from the command line

- Classes and dataclasses

  - Creating an Employee class
  - Make a dataclass version -> works!
  - Note that some of the example code is pretty bad (manager attributes in the Employee class)
  - Add an extra low quality exporter to factory example code (works!)

- Let's try to break it
  - Try stuff like "password =", "db_connection_string =", "api_key = " etc.

## My thoughts

Overall, I'm impressed. I find Copilot quite helpful with providing quick solutions to common software problems. I can imagine that as the tool gets better, it's going to save developers time.

This is not going to put out of a job, or make my channel obsolete. You still need to think about how to design your software and how to organize your code though. I wrote a guide to help you with this. You can get it for free at arjancodes.com/designguide. This describes the 7 steps I think about when designing a new feature or software application. It might help you structure your thoughts. Arjancodes.com/designguide.

I have a few concerns about Copilot.

- Legal issues (have already been mentioned by others)

  - Not a legal expert, and this has been covered before so I won't say too much about it. GitHub trained Copilot on publicly available code on GitHub. And they can do that under the terms and conditions that you agree to when you start using GitHub. But quite a lot of that code is under a Copy left license. In order to use that code, you need to include the license. Some people have been calling this Open Source software laundering for commercial use.
  - GitHub says that Copilot is mostly producing brand-new material, and that it only produces copies of learned code 0.1% of the time. But, there have been examples online of code suggestions that include fairly large amounts of code that clearly was copied because it even includes comments from the original source code. So if you notice code suggestions that look like they're blatantly copied, maybe you shouldn't use those just to be on the safe side.

- Quality issues

  - Since it's based on the code that's in current GitHub repos, there are quality issues (see example with Employee/management)
  - If developers simply accept code suggestions by Copilot without checking that it actually does what it needs to do, this might lead to a spiral of decreasing code quality. Because that generated code is committed and used by the algorithm to learn from and suggest to others. This is kind of similar to what's happening on social media where recommendation systems put people into bubbles of misinformation.
  - Of course this kind of thing also happens on Stack overflow - copy-pasting code without looking at what the code is doing. But at least there, you still have a kind of community control. With Copilot, you're on your own.
  - Not sure if Copilot has incorporated some kind of quality metric. Perhaps it can learn from the choices developers make when selecting which suggestion to use. But that might still lead to the decreasing quality spiral I mentioned earlier.

- Security issues
  - Many repos contain sensitive information such as DB credentials, API private keys, and so on. GitHub trains the models on public repos, where this is less of a problem, but that might change. Tools like Copilot are another reason to never put sensitive data in repositories, even if they are private.
  - Can a bad actor commit malicious code and trick the algorithm into suggesting that code to other developers who then use it? This opens up a new avenue for hackers to get into existing code.

Overall: it's an interesting new direction for software development. I'm not going to uninstall this yet and see how it feels when I use this for a longer period. I'm curious: do you see yourself using Copilot in your development process? Would you pay for this? Let me know what your thoughts are. Thanks for watching, take care and see you soon!
