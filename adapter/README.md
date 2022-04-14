# Class diagram

There are two versions of the classic Adapter pattern: object-based and class-based.

## Object-based version

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

## Class-based version

In the class-based version of the pattern, the Adapter _inherits_ from the Adaptee and adds extra methods to conform to the interface

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
