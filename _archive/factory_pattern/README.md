## About this video

This video introduces the Factory Pattern, a classic design pattern from the GoF book.

## Video outline

- The Factory Pattern is a classic pattern from the GoF book on Design Patterns. The goal of the factory pattern is to help write code that separates creation from use. In other words, you should create objects in another place than where you're using them. This is helpful, because by separating creation from use, you can write the code that uses the objects without knowing precisely what those objects are. And then later on, you can decide to replace the objects with something else without having to change the original code.

- Explain the before example. There are video and audio exporter codecs in the example. User is asked for desired output quality. Then, the desired exporters are created and the video/audio is exported.

- Analysis: the main function has many responsibilities. The code for selecting the various combinations of exporters is not great. If we want to add other exporters, other combinations of exporters, then we'd have to add more elif statements, leading to even weaker cohesion. There is also coupling because the main method is responsible for creating the actual exporters it has to know all the specific exporters.

- Create a ExporterFactory abstract class that constructs a combination of video/audio exporter for us.

- Create a few concrete factories (low, high, master).

- Add a read_factory method that constructs the factory from the user's input.

- Update the main function to retrieve the exporters from the factory.

- Overall, factories are really useful to separate creation from use. One of the strong points of factories is that they allow you to group objects that belong together in a logical way (like here: a low-quality setup, or a high-quality setup). So, they work well if you for example want to create a system that has various presets for something, or for example if you define sets of currencies, locale settings, and shipping costs for different countries in a sales system.

- Factories work less well if you need any combination of things. For example, if you want the user to specify the precise codecs instead of these fixed settings, because then you would need to create a factory class for each possible combination. In this case, it's better to use simple composition and dependency inversion as this allows for more flexibility while retaining the reduced coupling. See my recent video for an example of how to do that.
