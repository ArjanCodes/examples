## About this video

In this video, I talk about a more data-oriented version of the Factory pattern that allows you to create objects that you read from a JSON file. The advantage of this approach is that you can register and unregister various character types, without having to change the data loading code as well as the game character usage itself.

## Video outline

- Often, you want to extend code after it's been shipped. For example, if you build a game, you might want to release an update with new game characters, or you want modders to be able to plug in new types of characters in your game. In that latter case, you need a pattern that allows you to do this without changing any of the original code. This is a similar problem to building a system that allows for third-party plugin development. A second thing you often encounter, especially in games, is that these custom characters/extensions need to be created via a specification in the data.

- I'm going to show you a variety of the factory pattern, I'm calling this the 'plugin pattern' that completely separates creation of objects from their specification in the data.

- Explain the example first: simple game with a variety of characters (show JSON file with examples).

- Load the data from the file and print out the contents.

- Create a generic GameCharacter ABC, and then specific subclasses for each of the characters (except bard).

- Now the fun part: create a factory that can create these characters, without knowing their type. This is done via registering and unregistering creator functions (which in fact are class initializers)

- Now create the factory, register the characters and do something with the characters.

- Create a basic plugin loading mechanism, using importlib.

- Add an extra character 'bard'. For this, we don't have to change the factory class at all. We only need to create the specific subclass, and register it with the factory, and now we're able to use it. Using this plugin mechanism, we were able to extend the code without having to touch the original code! Isn't that neat?
