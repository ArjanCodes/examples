# Introduction

In this video, I'm going to talk about context managers in Python, how to use them and how to create your own. But, they also have some issues that you need to know about.

Let's dive in!

# What are context managers?

Context managers allow you to allocate and release resources precisely when you want to. The most widely used example of context managers is the with statement.

# Basic usage (screencast)

- Create SQLite context manager (showing both the class and the decorator syntax)

# Context managers and async (talking head)

Context managers also support async/await syntax. If you want to learn more about async (concurrent) operations in Python, check out [this] video.

# Context managers + async example (using aiosqlite, screencast)

# When to (not) use context managers

The main reason to use context managers is to help allocate and cleanup resources. This is helpful for example if you want to open a file, open and close a database connection, or open and close a network connection. If an error occurs, the context manager mechanism allows you to cleanup the resource. If you don't use context managers, you have to manually close the resource.

If you don't need to cleanup resources, there's no reason to use a context manager. In fact, you shouldn't. Because context managers are used with the 'with' statement in Python, this also results in a deeper code indentation level. Having an extra layer of indentation is not such a big problem, but things get messy when you have a chain of with statements, each creating different resources:

```python
with open_socket() as s:
    with open_file() as f:
        with open_database() as db:
            do_stuff(s, f, db) # ugh
```
