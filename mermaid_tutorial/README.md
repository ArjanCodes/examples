# Introduction

Generally, UML diagrams are quite useful for visualizing aspects of your code: flowcharts to describe user interactions, class diagrams to show structure of your code, and so on. The problem is, they're a pain to draw, even using tools that have specific support for them, like Draw.io.
And for that reason, I've been using them very little. But there's a tool I found recently that I think is going to change this. It's called [Mermaid](https://mermaidjs.github.io/). Today I'll show you how to use it to create UML diagrams really quickly.

Before that though, I want to talk a bit more about UML in general, whether it's really useful or not.

# Flowcharts

```mermaid
flowchart LR
    S[Start] --> A;
    A(Enter email address) --> B{Existing user?};
    B -->|No| C(Enter name);
    C --> D{Accept conditions?};
    D --> |No| A;
    D --> |Yes| E;
    B -->|Yes| E(Send email with magic link);
    E --> End;
```

# Sequence diagram

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant OAuthProvider
    participant Server
    Client->>OAuthProvider: Request access token
    activate OAuthProvider
    OAuthProvider->>Client: Send access token
    deactivate OAuthProvider
    Client->>Server: Request resource
    activate Server
    Server->>OAuthProvider: Validate token
    activate OAuthProvider
    OAuthProvider->>Server: Token valid
    deactivate OAuthProvider
    Server->>Client: Send resource
    deactivate Server
```

# Class diagrams

Most common relationships between classes: inheritance, aggregation, composition.

In mermaid:
<|-- Inheritance
\*-- Composition
o-- Aggregation

What's the difference between composition and aggregation? Aggregation and Composition are subsets of association meaning they are specific cases of association. In both aggregation and composition an object of one class maintains a reference to an object of another class. But there is a subtle difference:

- Aggregation implies a relationship where the child can exist independently of the parent. Example: an order refers to a customer. If you delete the order, the customer should still exist.
- Composition implies a relationship where the child cannot exist independent of the parent. Example: Car (parent) and Engine (child). Engines don't exist separate to a Car.

```mermaid
classDiagram
    SuperClass <|-- SubClass
    Order o-- Customer
    Car *-- Engine
```

```mermaid
classDiagram
    class Order {
        +OrderStatus status
    }
    class PaymentProcessor {
        <<interface>>
        -String apiKey
        #connect(String url, JSON header)
        +processPayment(Order order) OrderStatus
    }
    class OrderStatus{
        <<enumeration>>
        FAILED
        PENDING
        PAID
    }
    Order o-- Customer
    Customer <|-- BusinessCustomer
    Customer <|-- PrivateCustomer
    Customer o-- PaymentProcessor
    PaymentProcessor <|-- StripePaymentProcessor
    PaymentProcessor <|-- PayPalPaymentProcessor
```

# Entity-relationship diagram

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        String id
        String name
        String sector
    }
    ORDER ||--|{ LINE-ITEM : contains
    ORDER {
        String id
        String address
    }
    LINE-ITEM {
        String code
        String description
        int quantity
        int unitPrice
    }
```
