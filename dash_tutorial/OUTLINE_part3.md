# Dash video tutorial Part 3

In this part, I'm going to focus on the software design aspects, mainly looking at how to better separate the UI elements from the data processing. In principle, this is going to be a Model-View-Controller approach, where the pandas DataFrame is the model, the DataSource is the controller, and the Dash components are the View.

- Adding localization (dates and texts)
- Reducing coupling by introducing a DataSource class that encapsulates all the data processing
- Show further possibilities for decoupling by abstraction, notably:
  - In the year selection dropdown, we can also work with a list of strings instead of a data source
  - In general we could define a protocol class that abstracts away the specific data source implementation
