## About this video

This video is about Structural Pattern Matching, an upcoming feature of Python 3.10.

## Video outline

- Python 3.10 introduces a couple of interesting new features. One of the biggest features is Structural Pattern Matching. It's pretty powerful. I'm going to show you a few examples today of what you can do with this.

- Structural Pattern Matching looks a lot like the switch statement that is available in many other languages like Java or C++. Switch statements are generally easier to read than sequences of if-else statements. However, they also often point to issues in the design. If you need a complicated if-else or switch to handle all the different cases, then you might want to think about using a design pattern like a strategy instead.

- However, Structual Pattern Matching does way more than the switch statement in other languages. And that's why I think it's a very useful addition to Python. Let me show you what's possible in an example.

- Give a short overview of the example, which is a simple CLI.

- Version 1: very basic pattern matching using values only. Add a case 'other' that shows how to deal with default values. Also show you can use \_ if you don't actually need the value.

- Version 2: more advanced pattern matching. First split the command, and then use various patterns to detect commands (e.g. loading or saving files, quit with or without --force)

- Version 3: Show that you can add a condition to a case

- Version 4: Create a Command class that contains a command + arguments, and use that class in the pattern matching instead. Show that you can nest patterns, for example by adding a match inside the arguments list part of the Command objects.

- There are some caveats. The first caveat is that the cases are run from top to bottom. This means that the order in which you place the cases influences the result. Show an example with the quit command with or without parameters (switching them around results in the case with --force being completely ignored). The second caveat is that if you're using this as a traditional switch statement, your function probably has weak cohesion. Split things off this case and use something like the strategy pattern.

- Python 3.10 has other interesting new features as well such as a shorter syntax for union types. Together with Structural Pattern Matching, this opens up a lot of possibilities, including doing monadic error handling, a concept I discussed in an earlier video.
