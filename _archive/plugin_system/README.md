## Video outline

[talkinghead] In this video, I talk about the plugin architecture, which allows you to add functionality to an application, without changing a single line in the original code, including the imports.

Let's dive in!

If you want to learn more about software architecture and design, Skillshare, who is the sponsor of today's video, has some great classes on the subject.

Skillshare is an online learning community with thousands of inspiring classes for creators. Explore new skills, deepen existing passions, and get lost in creativity.

Skillshare has many classes on web development, programming in Python, software engineering, and software design.

Skillshare is curated for learning. There are no ads, and they're always launching new premium classes, so you can stay focused and follow wherever your creativity takes you.

Whether you're a beginner programmer or an experienced developer, Skillshare has classes that will help you learn and grow.

The first 1,000 of my subscribers to click the link in the description will get a 1 month free trial of Skillshare so you can start exploring your creativity today!

[screencast] Explain the example first: game with a variety of characters (show JSON file with examples, excluding the bard). Run the code and see what happens.

[talkinghead]

- Often, you want to extend code after it's been shipped. For example, if you build a game, you might want to release an update with new game characters, or you want modders to be able to plug in new types of characters or even entire levels in your game. In that latter case, you need a architecture that allows you to do this without changing any of the original code. This is what's called a plugin architecture.

- In this video, I'll show you how you can do this in Python. I'm going to modify the original code so that you can read objects from a JSON file and add new characters, by registering them as plugins and then dynamically importing the modules. The result is that you can write these plugins completely separate from the original code.

[screencast]

- First thing to do is to create a registration system, because at the moment, the available character types are chosen from in an if-statement. This allows us to dynamically changes which types of characters are available.

- Create a plugin loading mechanism, using importlib. Now we can load files dynamically. Let's look at an example.

- Add an extra character 'bard'. For this, we don't have to change the factory class at all. We only need to create the Bard class, and register it, and now we're able to use it. Using this plugin mechanism, we were able to extend the code without having to touch the original code! Isn't that neat? You can even add custom data and store that in the instance (change the instrument to test this).

- The plugin architecture is really powerful and allows for a lot of customization. Here I'm using it for loading custom game characters, but you can also use a similar mechanism to create custom GUIs for your plugins.

- Thanks again to today's sponsor, Skillshare. Don't forget to check them out via the link in the description. If you enjoyed this video, give it a like and consider subscribing to my channel. Thanks for watching, take care and see you next time!
