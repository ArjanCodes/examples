# Analysis of the current code

- Use snake case to comply with Python's PEP8 style guide
- in endscreen: no need to store winnerlabel in a member variable
- don't forget to add type hints
- the pos instance variable is actually not used anywhere, so you can remove it
- You're using inheritance to distinguish the various piece types. This might be nice to be able to override which piece has which valid moves. However, this also leads to loads of isinstance use, which makes the logic really hard to read. And if you ever decide that you want to use inheritance so that for example the queen can reuse some of the valid move computation from the rook or the bishop, you're in trouble because you also rely on inheritance to distinguish between the pieces themselves.
- there's a lot of duplication in the piece subclasses
- call GUI main so we know what the entry point of the application is
- populatewithfen has a lot of duplication
- In logic, you're using 'y' for a piece and 'x' for an index which is confusing
- The logic has lots of Law of Demeter violations. It needs to know details of the board data structure which makes it hard to read.

## Refactoring idea 1: change the Piece inheritance hierarchy to a single class

## Refactoring idea 2: create a Board class that has a few useful methods

## Split out the valid moves functions

Show an example of how to do it for one piece: the rook.

## A few final discussion points

- There's still a lot of duplication in the code that checks what the valid moves are. It's probably better to split this up more. For example, you could define types of moves (horizontal and vertical moves, diagonal moves, knight moves, etc.) and then each piece has a combination of these groups instead of computing it for every piece separately. You can then also use a single function to compute the valid moves.

- I didn't have time to dive deeper into the ChessLogic class. By moving to a separate Board class you can already simplify the logic a bit since it can use the methods from the Board class. Also because the Piece inheritance is no longer there, you don't need all those isinstance calls everywhere. I do think there's still more work to be done in this class though. The methods are quite long and should be split up. And things can probably be generalized more by rethinking how the logic is structured. If you have any suggestions, post them in the comment section.
