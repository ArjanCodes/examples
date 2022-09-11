# Analysis of the current code

- Use snake case to comply with Python's PEP8 style guide
- in endscreen: no need to store winnerlabel in a member variable
- don't forget to add type hints
- the pos instance variable is actually not used anywhere, so you can remove it
- there's a lot of duplication in the piece subclasses
- call GUI main so we know what the entry point of the application is
- populatewithfen has a lot of duplication
- In logic, you're using 'y' for a piece and 'x' for an index which is confusing
