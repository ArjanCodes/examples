# Code roast video

It's time for another code roast!

## Analysis

A few obvious ones:

- Lots of global variables. This makes it hard to separate things into different files. You don't know which parts use which global variables.
- Wildcard tkinter import. This also makes it hard to separate things, because when you're moving a class to another file, you have no idea what imports you'll be missing, and you can't search for "tk." or "tkinter." to find them.
- All classes are in the same file which makes it really hard to refactor.
- Creating and running the game should be put into a main function.
- Empty except blocks are really bad, never use this because it hides other errors.

Other things:

- Game class has way too many responsibilities. It's responsible for creating the objects in the game as well as managing the overall game loop. Duplication in updating and painting objects.
- Objects in the game directly access other objects, which introduces coupling in both the structure of the Game class, as well as specific implementations of game objects. There's also a risk of breaking the game loop in this way, because event handling happens outside of the loop (so it may occur during an update for example which will lead to race conditions).
- We need a proper game engine!

## A few quick bits

- Wavegenerator update indent level
- NextWaveButton if statement `if self.x <= x <= self.xTwo and self.y <= y <= self.yTwo:'
  Change to if self.x <= x <= self.xTwo and self.y <= y <= self.yTwo: and can_spawn property
- Classes don't need to inherit from object anymore in Python 3
- Super calls can be made shorter
- `if selectedTower == "<None>":` -> use None instead
- self.RUN is True (is True is not needed, and don't use capital letters if something can change).

## About game engines

A few common problems when you're creating a game:

- You have lots of objects at certain positions in the game. These objects need to be updated and drawn on the screen. The order in which you draw them matters, and so does the order in which you update them.
- Sometimes, objects need to communicate (e.g. when you press the 'spawn' button, the spawn generator should create new enemies). Ideally, you should be able to do this without objects knowing anything about each other.
- You need to process player input like mouse motions, or key presses, and that should integrate into the update/paint cycle without breaking it.
- Some objects (like the wave generator), depend on ticks to spawn enemies at a certain rate. If you update the framerate for faster computers, now the monster will spawn faster as well, which is not what you want. Game engines often offer some kind of time mechanism that allows you to deal with time in various forms (e.g. game time, real time, etc.). What we need here is a better mechanism to do something after a delay that also integrates well into the update/paint loop. A possible solution is to add a scheduling mechanism to let the game engine call a function after a certain time or if a condition is met.

## Refactoring the tower defense game

- Cleanup the empty try/except blocks. TrackingBullet length fix.
- Create a separate game.py file and put all the generic game code related to updating and drawing in a game loop there.
- Improve running the loop by cancelling the timer (using after_cancel), and adding an option to define the timestep.
- Adding a game object list and update/paint the objects as part of the game loop. Update happens in reverse order to Paint so that elements on top can process input first. Briefly talk about possible extensions here: 1) having hierarchies of game objects, where each is responsible for updating and drawing its own sub-objects. Each element in the hierarchy basically represents a graphics layer. 2) special game object structures like a grid could also be standardized. 3) Dealing with positioning (local vs. global coordinates) in the game engine. 4) add a scheduling mechanism to do something after a certain delay/condition is met that is part of the update mechanism 5) add event posting and handling
- Update TowerDefense to add a few game objects. Do this in a separate initialize method. Use add_object for Mouse and Map, not yet for SpawnGenerator. You could also consider simply creating game objects outside of the class in a separate initialize function that calls the add_object method for each object.
- Add a basic game state to TowerDefense and use that for communicating instead of directly accessing game objects. As a result, we can now also make spawngenerator a simple game object.

## Final thoughts

- Obviously, the refactor is far from finished. Having a basic game engine setup already helps, and now you can start separating out the various different objects and combine them in a more loosely coupled way.
