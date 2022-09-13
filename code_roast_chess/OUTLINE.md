# Code Roast: Chess

It's been a little while, but now it's time for a ... code roast!

Today I'm going to roast a Chess game.

When I did these code roasts in the past I often had to cut them up in 2 or even 3 different parts for them not to be way too long. I've noticed that splitting videos up in parts doesn't work well on YouTube. The first part of a series often doesn't do well because quite a few of you wait until all the parts are out, which I totally understand. And then subsequent parts get lesser and lesser views because not everyone wants to watch the whole thing, which also makes sense. But this results in these videos performing really badly which on YouTube means less people are going to find the content. And that's a pity.

So, this is an experiment. I am going to roast the code and provide a deep review because that's I think the part you learn the most from. And then instead of doing a full refactoring, I'm going to zoom in on some of the things I mention in the review and show you an alternative way of setting it up.

# Analysis of the current code

- in endscreen: no need to store winnerlabel in a member variable
- don't forget to add type hints
- the pos instance variable is actually not used anywhere, so you can remove it
- You're using inheritance to distinguish the various piece types. This might be nice to be able to override which piece has which valid moves. However, this also leads to loads of isinstance use, which makes the logic really hard to read. And if you ever decide that you want to use inheritance so that for example the queen can reuse some of the valid move computation from the rook or the bishop, you're in trouble because you also rely on inheritance to distinguish between the pieces themselves.
- there's a lot of duplication in the piece subclasses
- call GUI main so we know what the entry point of the application is

logic.py:

- Instead of using integers like 0 or 1 to represent the colors, use enums. This make the code easier to read and you don't need a comment to explain what each value means.
- populateWithFen has a lot of duplication. And also, this is a method that creates a board and pieces. It doesn't belong in the logic class.
- In many methods (for example `check_for_check`), you're using 'y' for a piece and 'x' for an index. Don't do that, it's confusing. When I see x and y in a code, I expect them to be of the same type, and most often integers or floats.

- There are lots of Law of Demeter violations in this class. What is the Law of Demeter? It states that each unit of code should have only limited knowledge about other units. Here, your code needs to know details of the board data structure which makes it hard to read. On top of that, there are a bunch of isinstance calls that also require you to know the inheritance hierarchy.
- In particular, `move_piece` is way too large and filled with these violations. As a result this method is very hard to understand and if there's a bug, you're going to have to spend a lot of time figuring out what is going on.
- The `check_for_mate` method is hard to read due to deep indentation. You can use guard clauses here to improve things.

Minor things:

- Use snake case to comply with Python's PEP8 style guide

## Refactor 1: Guard clauses

Refactor `check_for_mate` to use guard clauses (see `check_for_mate.py`).

## Refactor 2: change the Piece inheritance hierarchy to a single class

- Create enums for the color and the piece types
- Create a Piece dataclass
- Add a few simple methods like move_to and promote_to_queen
- Add an `image` property that's generic

## Refactor 3: create a Board class that has a useful methods

- Create the necessary type definitions
- Create the board class
- Add a few useful methods such as place, piece, empty and find_king

## Refactor 4: Fill the board from a FEN string

- Now that we have Board and Piece classes, you can use a static method to create instances of them from a FEN string. This is much cleaner that doing it in the logic class.

## Refactor 4: Split out the valid moves functions

Show an example of how to do it for one piece: the rook.

## A few final discussion points

- There's still a lot of duplication in the code that checks what the valid moves are. It's probably better to split this up more. For example, you could define types of moves (horizontal and vertical moves, diagonal moves, knight moves, etc.) and then each piece has a combination of these groups instead of computing it for every piece separately. You can then also use a single function to compute the valid moves.

- I didn't have time to dive deeper into the ChessLogic class. By moving to a separate Board class you can already simplify the logic a bit since it can use the methods from the Board class. Also because the Piece inheritance is no longer there, you don't need all those isinstance calls everywhere. I do think there's still more work to be done in this class though. The methods are quite long and should be split up. And things can probably be generalized more by rethinking how the logic is structured. If you have any suggestions, post them in the comment section.
