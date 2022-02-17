# Introduction

In this video I'm going to refactor a simplified Battleship game. Thanks to Sax for providing the code for this roast. Sax asked me to be extra mean in this roast. So, just to be sure: you suck, you write worse code than an intern with a hangover. And before I started recording this video, I killed three puppies. Not those three though, I could never do that, they're too cute! Awwww...

By the way, if you want your code to be roasted on the channel. If you like feeling violated, feel like there's a void where once there was your soul. Join my Discord server, and submit your code if you dare.

Before we take a closer look at the Battleship game, I want to give you something. It's a free guide that helps you make better design decisions. It contains the 7 steps I take whenever I design a new piece of software. Hopefully it helps you avoid some of the mistakes I made in the past. So, get your copy for free at arjancodes.com/designguide. The link is also in the description of this video.

Now let's dive into the code.

# Analysis of the game code

I'll start with an analysis of the game, and then I'll show you how to refactor the code to make it more readable and maintainable.

- A lot of things are stored in the Game class as instance variables that are not needed. For example, there's no reason to store the guess_row and guess_col values as these are only used locally in a particular player turn.
- Some data might not be optimally represented. For example, you store the number of guesses a player still has in a list of integers. But is that really needed? You play this game in rounds, so the number of guesses can be computed from which round you're in.
- Because of the two things above, the Game class actually contains a lot of instance variables, which can be simplified.
- There are some functions that do not directly rely on instance variables in Game. For example, the function for reading user input could be separated out of the Game class. This way, you can use this function in other parts of the code. For example, battleship_run reads the number of players and has a very similar structure, so you could reuse the integer reading function there if you split it out of the Game class.
- Talking about battleship_run: the name of the function is wrong, because the only thing it does is read the number of players. It doesn't actually run the game. Same for 'create_matrix'. In principle, the board is a matrix, but a very specific one. So we should call this create_board to better reflect that specificity (is that English?).
- In create_matrix, you're using deepcopy, but it's not needed since you create a new board anyway.
- Printing the board can be done more efficiently, and 'return None' isn't needed.
- if/else statements in player_guesses and game_logic can be rewritten to decrease code indentation, making the code more readable.
- You can use f-strings for easier string interpolation and formatting.
- It's better to create a separate main function instead of creating variables and running code in the 'if **name** == "**main**":' block. This way, you don't pollute the global/module scope with variables.
- The game logic directly accesses and modifies the board. This makes the code harder to read. I would introduce an abstraction layer to hide the implementation details of the board from the game logic. Adding a few methods to the Game class would solve this.
- Multiline comments/docstrings should be below a function or method definition instead of above it. They also shouldn't contain "opinions" like: "I think this is easy to read".
- There are some numbers in the code like the board size and the number of guesses that are hardcoded. It's better to make these variables constants and define the at the top of the module (or even define them completely outside of the code in a config file).
- Finally, types can be used more strictly to clarify what a function expects and returns.

# Game refactoring

- Separating input and printing from the game
- Use types more explicitly
- Early exit from a method
- Create properties and methods to increase readability (e.g. to check if a guess is valid)
- Rename battleship_run to something more meaningful (ie read_nr_players)

# Final thoughts

You can potentially separate out the usage of constants more from the Game class if you wanted to. For example, the number of guesses could be passes to the Game initializer. Or, you could determine the board size from the board itself instead of using the constants. Or store those constants in the object and use that.
