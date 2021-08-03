## Video outline

In this video, I talk about the plugin architecture, which allows you to add functionality to an application, without changing a single line in the original code, including the imports. Let's dive in!

This architecture is widely used. For example, many graphics programs use such an architecture to allow you to extend the functionality of a piece of software
In this video, I talk about a more data-oriented version of the Factory pattern that allows you to create objects that you read from a JSON file. The advantage of this approach is that you can register and unregister various character types, without having to change the data loading code as well as the game character usage itself.

- Explain the example first: game with a variety of characters (show JSON file with examples, excluding the bard). Run the code and see what happens.

- Often, you want to extend code after it's been shipped. For example, if you build a game, you might want to release an update with new game characters, or you want modders to be able to plug in new types of characters in your game. In that latter case, you need a architecture that allows you to do this without changing any of the original code. So what I'm about to show you is not really a design pattern. It has elements of the factory pattern, but it's more architectural.

- First thing to do is to create a registration system, because at the moment, the available character types are chosen from in an if-statement. This allows us to dynamically changes which types of characters are available.

- Create a plugin loading mechanism, using importlib. Now we can load files dynamically. Let's look at an example.

- Add an extra character 'bard'. For this, we don't have to change the factory class at all. We only need to create the Bard class, and register it, and now we're able to use it. Using this plugin mechanism, we were able to extend the code without having to touch the original code! Isn't that neat? You can even add custom data and store that in the instance (change the instrument to test this).

- The plugin architecture is really powerful and allows for a lot of customization. Here I'm using it for loading custom game characters, but you can also use a similar mechanism to create custom GUIs for your plugins.
