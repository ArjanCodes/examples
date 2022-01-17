# Bridge pattern

In this video, I'm going to talk about the Bridge pattern and show you how to build it in Python. But, I'm not just going to build the standard Bridge pattern. No, no, no, we're going to do things the Pythonic way.

Before we dive in, I have something for you: a free guide to help you make better design decisions. You can get it at arjancodes.com/designguide. It's a PDF file, to the point, explaining the steps I take when I design a new piece of software. Hopefully, it's helpful to you. So, arjancodes.com/designguide. The link is also in the description of the video.

Consider an application that can stream to different streaming services (YouTube, Twitch). And you also have different streaming devices that link to the streaming services (webcams, cameras, microphones). You want to be able to add new streaming devices without having to change any code in the streaming services, and the other way around. How do you set that up?

That's where the Bridge pattern comes in. This pattern introduces two separate hierarchies of abstraction. In the Gang Of Four book, I find the way that this pattern is presented is a bit confusing. They talk about an abstraction (with refined abstractions), and an implementation (with concrete implementation subclasses). But it's not really clear why one hierarchy is an abstraction and the other an implementation. I prefer to keep things simple and just say that there are two hierarchies and there's a dependency between them, but you can introduce new variations in each hierarchy independently from each other.

Let's take a look at the Bridge pattern class diagram:

```mermaid
classDiagram
    class Abstraction {
        <<abstract>>
    }
    RefinedAbstraction1 --|> Abstraction
    RefinedAbstraction2 --|> Abstraction
    class Implementation {
        <<abstract>>
        +implementation()
    }
    Abstraction o-- Implementation : uses
    Implementation <|-- ConcreteImplementation1
    Implementation <|-- ConcreteImplementation2
    ConcreteImplementation1: +implementation()
    ConcreteImplementation2: +implementation()
```

What makes the Bridge pattern interesting is that the coupling occurs on the abstract level: the Abstraction (which is abstract) uses the Implementation (which is also abstract). The coupling happening on this level is what lends the Bridge pattern its power.

# Bridge pattern (simple version with Protocol classes)

Updated class diagram:

```mermaid
classDiagram
    class StreamingService  {
        <<abstract>>
        +start_stream()
        +stop_stream()
        +fill_buffer()
    }
    YouTubeStreamingService --|> StreamingService
    TwitchStreamingService --|> StreamingService
    class Device {
        <<abstract>>
        +get_buffer_data()
    }
    StreamingService o-- Device : uses
    Device <|-- Webcam
    Device <|-- DSLRCamera
    Webcam: +get_buffer_data()
    DSLRCamera: +get_buffer_data()
```

# Bridge pattern (using a function)

# Bridge pattern using an ABC and device list (talking head)

The Bridge pattern is actually a good use case for not using a Protocol class, but using an ABC. The main reason is that we can use the ABC to define the relationship between the Abstraction and the Implementation in the pattern. So in this case, the relationship between the streaming service and the device. With protocols, this isn't possible because there's no inheritance relationship, only duck typing.

Let's also introduce a little variety. Wouldn't it be nice to have a list of devices instead of a single device. By using ABCs, we can define this in a single place (in the ABC) and then use that directly in any of the streaming services. Let's see what that looks like.

# Bridge pattern with device list and ABC (screencast)

I hope you enjoyed this video! Give it a like if you did, consider subscribing to my channel if you want to learn more about software development and design. Thanks for watching, take care, and see you soon!
