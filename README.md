## About this repo

In this repository, I put all the projects/topics that I'm working on for the ArjanCodes channel. Normally, each video will have its own folder. Once a video has been published, to keep things clean here I'll remove the folder from this repository and put the final code in a separate repository that the viewers can download.

For larger projects or series, I might put multiple videos together in a separate subfolder, e.g. code_roasts/yahtzee or building_an_api/security.

## General guidelines for Python code examples

I'd like to create a certain level of consistency in the Python videos and make sure that the code style is the same everywhere, and also easily understandable for intermediate-level software developers. Note that this is different from "regular code". The aim is not to write production-level code (then a guideline might be to reach x% of test coverage for example), but to write code that is consistent over the different videos, close enough to what is best practice in a production environment, but at the same time doesn't obfuscate or overcomplicate the concepts that the example needs to convey.

This is what I have until now:

- Use the black autoformatter on all Python code I write.
- Use pylint. Wherever possible, make sure that code has no pylint issues.
- Mainly rely on built-in modules for the examples (e.g. use dataclasses as opposed to Pydantic). Preferably, I'd like my examples to run right off the bat, without having to install any dependencies. Some videos will cover specific modules though, and then of course the viewer will need to install the dependencies.
- For built-in modules, use `from X import Y, Z` instead of `import X` and then later on `X.Y`. For third party modules, the other way around.
- Not really sure what the best way is to deal with referencing local imports. I could add an `__init__.py` file to the main folder, I could do something like `import X from .my_file`. Any thoughts on what's the cleanest way to do this?
- Always use snake case.
- The editor I use is VSCode (for Python, but also for examples in other languages).

Feel free to make any suggestions for improving this.
