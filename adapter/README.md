# Intro

This video covers the Adapter pattern and a few variations of it. I'll start with the classic pattern which relies on classes. But then I'll show you how to take this a step further by taking the idea of the pattern and using modern Python features to achieve the same effect, but with less code. Let's dive in!

# Explain the example code

This application relies on a config file written in JSON format. You'd like to allow for the possibility to read a config from an XML file as well, but you realize that existing libraries for getting data from an XML structure don't directly fit into your application. This is where the Adapter comes in.

# Goal of the Adapter pattern (Talking head couch)

The goal of the Adapter pattern is to adapt an existing system so you can use it in your application. You do this by creating a layer (that's called the Adapter) between the existing system and your application. It's a bit like when you have something that has a micro USB input used for charging, but you have a USB-C charger. The cable doesn't fit, but you can use an adapter that you put between the USB-C cable and the Micro USB input. That's what the Adapter pattern does, but then in software.

There are two versions of the classic Adapter pattern: object-based and class-based.

# Object-based version (Screencast)

In the object-based version of the pattern, the Adapter maintains an instance of Adaptee and calls operations on the instance.

```mermaid
classDiagram
    class Client {

    }
    class Target {
        <<interface>>
        +operation()

    }
    class Adapter {
        +operation()
    }
    class Adaptee {
        +specificOperation()
    }
    Client o-- Target : uses
    Target <|-- Adapter
    Adapter o-- Adaptee
```

# Change the example to use an object-based adapter (Screencast)

# Class-based version (Screencast)

In the class-based version of the pattern, the Adapter _inherits_ from the Adaptee and adds extra methods to conform to the interface.

```mermaid
classDiagram
    class Client {

    }
    class Target {
        <<interface>>
        +operation()

    }
    class Adapter {
        +operation()
    }
    class Adaptee {
        +specificOperation()
    }
    Client o-- Target : uses
    Target <|-- Adapter
    Adapter <|-- Adaptee
```

# Taking the pattern to the next level (Talking head main)

The idea of the pattern is that it forms a adaptation layer between the existing system and your application. There's no particular reason to use a class for that. In fact, if you use a function that's partially applied, you can achieve the same adaptation, shorten the code at the same, and boast about being a functional programming elitist.

# Change the code to use function + partial

# Outro
