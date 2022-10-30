In this video, I’m going to talk about different GUI architectures. One you might have heard of is MVC, or: Model-View-Controller. But there are others as well, such as Model-View-Presenter, or Model-View-ViewModel. So, what’s the difference? And which one should you use? Do you even have a choice?

Unfortunately, there is no clear consensus of what these different architectures are exactly. I’ve looked up a bunch of different articles over the last weeks trying to find the “right” definition of each, but I found a lot of contradictions and people going to war over the details.

So, I’ve tried to distill the main differences between these architectures into three examples of the same, relatively simple, GUI application, but each time, setup slightly differently. I’ll then highlight what I think is the main distinctive feature of the particular architecture.

It may not always be completely “correct” because I’m also dependent on how the different GUI frameworks operate. I’m going to use Tkinter to show the difference between MVC and MVP, and I’ll use PyQt with a UI definition file to illustrate MVVM.

## MVC

MVC stands for Model-View-Controller. It was created by Trygve Reenskaug while working on Smalltalk-79. In his design, a Model represents the knowledge in the system. A View is a visual representation of the Model, retrieving data from the Model to display to the user and passing requests back and forth between the user and the Model. A Controller is an organizational part of the user interface that lays out and coordinates multiple Views on the screen, and which receives user input and sends the appropriate messages to its underlying Views.

Smalltalk-80 supports an evolved version of MVC. Here a `View` represents some way of displaying information to the user, and a `Controller` represents some way for the user to interact with a `View`. A `View` is also coupled to a model object, but the structure of that object is left up to the application programmer. A paper from 1988 on Smalltalk-80 defined a view as covering any graphical concern, with a controller being a more abstract, generally invisible object that receives user input and interacts with one or many views and only one model.

Showing all of these different varieties is hard, because we’re also dependent on what is possible with the GUI libraries in Python. So, let me do an attempt at showing how a version of MVC works when using Tkinter. In this version, the View is the graphical representation, the Model is the system knowledge, and the controller passes messages between the user and the model, and instructs the view to update itself.

_Show MVC example._

So, what about Django? Well, according to the Django website, they call their architecture a MTV (Model-Template-View) architecture. Quote from their website: “In Django, a view describes which data is presented, but a view normally delegates to a template, which describes *how* the data is presented.” The “controller” is the framework itself: the machinery that sends a request to the appropriate view, according to the Django URL configuration. (see: [https://docs.djangoproject.com/en/3.1/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names](https://docs.djangoproject.com/en/3.1/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names)). The way that Django sets up their architecture is related to how Martin Fowler defined the MVC architecture in 2003 where an "input controller" receives a request, sends the appropriate messages to a model object, takes a response from the model object, and passes the response to the appropriate view for display.

In the end, we can debate all day about the intricacies of what a view, controller, model, template, or controller is, the goal is to get the job done in a logical way.

## MVP

Regardless of which version of MVC you use, a criticism of the pattern is that the view is coupled directly to the model. You can also clearly see that in my example. There’s a lot of coupling between View, Controller and Model. An evolution of MVC that tries to solve this is MVP. MVP stands for Model-View-Presenter. In this case, the Controller is called a Presenter and it lies between the Model and the View. There’s also an abstraction layer between the Presenter and the View. As a result, the coupling between View and Model is now gone, and the Presenter is coupled to the View via an abstraction layer. In the example, I’ve used two abstractions (protocols) to completely decouple the Presenter from the View.

The nice thing about this approach is that if we change things in the Model, we now only need to update the Presenter as it forms a layer between the Model and the View.

_Show MVP example._

## MVVM

Model–view–viewmodel (MVVM) facilitates the separation of the development of the graphical user interface (GUI; the view), often via a markup language, from the development of the business logic or back-end logic (the model) such that the view is not dependent upon any specific model platform.

- *Model* refers either to a domain model, which represents real state content (an object-oriented approach), or to the data access layer, which represents content (a data-centric approach).
- As in MVC and MVP, the *view* is the structure, layout, and appearance of what a user sees on the screen. It displays a representation of the model and receives the user's interaction with the view (mouse clicks, keyboard input, screen tap gestures, etc.), and it forwards the handling of these to the view model via data binding (properties, event callbacks, etc.) that is defined to link the view and view model.
- The *view model* is an abstraction of the view exposing public properties and commands. Instead of the controller of the MVC pattern, or the presenter of the MVP pattern, MVVM has a *binder*, which automates communication between the view and its bound properties in the view model.

The main difference between the view model and the Presenter in the MVP pattern is that the presenter has a reference to a view, whereas the view model does not. Instead, a view directly binds to properties on the view model to send and receive updates. To function efficiently, this requires a binding technology or generating boilerplate code to do the binding.

A nice example of a GUI library that (kinda) supports this is PyQt. In PyQt, we have a .ui file that represents the structure and layout of the view (which is created from this file by the framework). We then have a view-model class that contains the bound properties and objects. If we change any of these, the view is updated automatically. Strictly speaking, this might not be entirely true since I expect that under the hood, PyQt simply creates the UI class from the .ui file and then you use that directly, but it’s the closest to MVVM I was able to get in Python, without resorting to exotic packages that are more proof of concepts than actually useable.

_Show MVVM example._

I hope you enjoyed this video and that it gave you an idea of what each of these architectures mean. MVP, or something close, is my preferred starting point. However, the exact architecture you should use in a particular situation is not written in stone. The most important thing to remember is to separate things in a GUI application and not put everything into a single huge file. Where you put those lines of separation depends on the GUI platform you use, how opinionated it is, and which flavor of architecture you personally prefer.
