# Code Roast: Chess

It's been a little while, but now it's time for a ... code roast!

Today I'm going to roast a Chess game. Thank you, Adam, for sharing this example.

When I did these code roasts in the past I often had to cut them up in 2 or even 3 different parts for them not to be way too long. I've noticed that splitting videos up in parts doesn't work well on YouTube. The first part of a series often doesn't do well because quite a few of you wait until all the parts are out, which I totally understand. And then subsequent parts get lesser and lesser views because not everyone wants to watch the whole thing, which also makes sense. But this results in these videos performing really badly which on YouTube means less people are going to find the content. And that's a pity.

So, here is an experiment. I am going to do a detailed code review because that's I think the part you learn the most from. But then instead of doing a full refactoring which takes a lot of time, I'm going to zoom in on some of the things I mention in the review and show you an alternative way of setting it up. I don't know if that works, it's an experiment. Let me know in the comments what you think.

For me, doing these code roasts have also helped me become more critical of my own code. I really encourage you to do more code reviews. It's going to open your mind. I tell ya, the b-roll is getting out of hand. Now, how do you become better at this. You might want to check out my free workshop on Code Diagnosis that teaches you a three-factor framework that helps you focus on what's important. Go to arjan.codes/diagnosis to get access. The workshop demonstrates how it works by looking at code from existing Python packages that are used in production. You're probably using one of these packages yourself. So, arjan.codes/diagnosis, the link is also in the description of this video.

Now, let's take a look at this chess game.

# Explain the example code

# Analysis of the current code

GUI.py:

- rename this file to `main.py` so we know what the entry point of the application is
- The class contains hardcoded values like a FEN string in `init_game` or the colors in the initializer. It's better to move these out of the class into constants so they're in one place which makes it easier to manage.
- The super class initialization is done halfway the initializer. Do it either as the first line or as the last line. Also, don't call Frame.**init** but super().**init**. That way the super class init call isn't directly dependent on the Frame type.
- commandHandler contains quite specific game logic. That doesn't belong in the GUI class.
- in endscreen: no need to store endwindow, winnerlabel, retrybut in a member variable here. The end screen should probably be a separate class component. This makes the GUI class a bit shorter.
- Use more precise type hints: if you write "list" as a type hint, also define what kind of list
- Sometimes pos seems to be a list, sometimes a tuple. It's even the question whether you shouldn't simply use an x and a y value instead to keep things simple.
- The GUI code is creating two new buttons and placing them them on top of the old ones every time a move is made. Also every time you refresh, you make a new PhotoImage. All these piled up buttons and images are destroyed only when a new game is started. This is very inefficient. You can reuse buttons and images instead of creating them new every time.

pieces.py:

- You're using inheritance to distinguish the various piece types. This might be nice to be able to override which piece has which valid moves. However, this also leads to loads of isinstance use, which makes the logic really hard to read. And if you ever decide that you want to use inheritance so that for example the queen can reuse some of the valid move computation from the rook or the bishop, you're in trouble because you also rely on inheritance to distinguish between the pieces themselves.
- there's a lot of duplication in the piece subclasses
- the pos instance variable is actually not used anywhere so you could remove it

logic.py:

- Instead of using integers like 0 or 1 to represent the colors, use enums. This make the code easier to read and you don't need a comment to explain what each value means. Same for the `STATUS` variable (which should be lowercase since it's an instance variable).
- populateWithFen has a lot of duplication. And also, this is a method that creates a board and pieces. It doesn't belong in the logic class.
- In many methods (for example `check_for_check`), you're using 'y' for a piece and 'x' for an index. Don't do that, it's confusing. When I see x and y in a code, I expect them to be of the same type, and most often integers or floats.

- There are lots of Law of Demeter violations in this class. What is the Law of Demeter? It states that each unit of code should have only limited knowledge about other units. Here, your code needs to know details of the board data structure which makes it hard to read. On top of that, there are a bunch of isinstance calls that also require you to know the inheritance hierarchy.
- In particular, `move_piece` is way too large and filled with these violations. As a result this method is very hard to understand and if there's a bug, you're going to have to spend a lot of time figuring out what is going on.
- The `check_for_mate` method is hard to read due to deep indentation. You can use guard clauses here to improve things.

Minor things:

- Use snake case to comply with Python's PEP8 style guide

## Refactor 1: Guard clauses

Refactor `check_for_mate` to use guard clauses (see `refactoring_ideas/check_for_mate.py`).

## Refactor 2: change the Piece inheritance hierarchy to a single class

(`refactoring_ideas/pieces.py`)

- Create enums for the color and the piece types
- Create a Piece dataclass
- Add a few simple methods like move_to and promote_to_queen
- Add an `image` property that's generic

## Refactor 3: create a Board class that has a useful methods

(`refactoring_ideas/board.py`)

- Create the necessary type definitions
- Create the board class
- Add a few useful methods such as place, piece, empty and find_king

## Refactor 4: Fill the board from a FEN string

(`refactoring_ideas/board.py` and `refactoring_ideas/pieces.py`)

- Now that we have Board and Piece classes, you can use a static method to create instances of them from a FEN string. This is much cleaner that doing it in the logic class.

## Refactor 5: Split out the valid moves functions

(`refactoring_ideas/moves.py` and `refactoring_ideas/board.py`)

- Show an example of how to do it for one piece: the rook.
- Add a dictionary to `board.py` to map the piece type to the function that gets the valid moves
- Add a Board protocol class to `moves.py` to provide some separation.

## A few final discussion points

- There's still a lot of duplication in the code that checks what the valid moves are. It's probably better to split this up more. For example, you could define types of moves (horizontal and vertical moves, diagonal moves, knight moves, etc.) and then each piece has a combination of these groups instead of computing it for every piece separately. You can then also use a single function to compute the valid moves as it simply combines move groups in this case.

- I didn't have time to dive deeper into `move_piece` method. By moving to a separate Board class you can already simplify the logic a bit since it can use the methods from the Board class. Also because the Piece inheritance is no longer there, you don't need all those isinstance calls everywhere. There's still more work to be done in the ChessLogic class though. The methods are quite long and should be split up. And things can probably be generalized more by rethinking how the logic is structured. If you have any suggestions, post them in the comment section.

Hope you enjoyed this roast. Thanks again, Adam for supplying the code for this one. Give this video a like, subscribe to the channel if you want to learn more about software design and development. If you enjoyed this roast, you might also like this one where I refactor a Rock Paper Scissor Lizard Spock Halbrand game (okay no Halbrand). Thanks for watching, take care and see you next week.
