# Dash video tutorial Part 3

## Introduction (talking head)

Here's the final part of the Plotly and Dash tutorial miniseries. I'm going to take things a step further in today's version of the code. I'm going to add support for internationalization (which really hard to pronounce) and I'm going to change the design to better separate the data from the UI components. You'll find the final version of the code on GitHub, the link is in the description.

A crucial part of making design improvements to the code is to have a better understanding of the problem you're trying to fix. In fact, being able to diagnose code is one of the most important skills you should have as a software developer. But where do you start? Well, I've created a Code Diagnosis workshop where I teach you the most important things to look at when you want to improve existing code. And I'm giving you access for free. You can sign up for the workshop at arjan.codes/diagnosis. It's an in-depth video workshop that contains a ton of useful advice and practical code examples so you can apply the ideas right away. So, sign up via arjan.codes/diagnosis, the link is also in the description.

## Screencast

- Adding localization (dates and texts)
- Reducing coupling by introducing a DataSource class that encapsulates all the data processing
- Show further possibilities for decoupling by abstraction, notably:
  - In the year selection dropdown, we can also work with a list of strings instead of a data source
  - In general we could define a protocol class that abstracts away the specific data source implementation
