# Introduction

In this video, I'm going to talk about context managers in Python, how to use them and how to create your own. But, they also have some issues that you need to know about.

Let's dive in!

# Explain the example without context manager (screencast)

# What are context managers?

Context managers allow you to to control setup and teardown of any sort of resource in way that minimizes the chance of you forgetting to do the teardown, especially in the presence of exceptions.

If you've ever opened a file in Python, you've probably used the with statement to manage the file. This is a context manager, and it's a good way to manage resources.

```python
with open('file.txt') as f:
    f.read()
```

Let's look a bit closer at what's happening in a with statement:

```python
with EXPRESSION as VARIABLE:
    DO SOMETHING
```

This is what's happening behind the scenes:

```python
manager = (EXPRESSION)
enter = type(manager).__enter__
exit = type(manager).__exit__
value = enter(manager)
hit_except = False

try:
    VARIABLE = value
    DO SOMETHING
except:
    hit_except = True
    if not exit(manager, *sys.exc_info()):
        raise
finally:
    if not hit_except:
        exit(manager, None, None, None)
```

The SQLite connection can itself be used as a context manager, like so:

```python
with sqlite3.connect('application.db') as conn:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blogs")
```

The advantage here is that the connection will automatically roll back commit or rollback transactions but the connection object does not automatically close so it should be closed manually afterwards. And then we'd still have to make sure that the connection is closed in all cases (even if an exception is raised).

The nice thing about Python is that we can create our own context managers. Let's create one for the SQLite example, that automatically closes the connection for us.

# Basic usage (screencast)

- Create SQLite context manager (showing both the class and the decorator syntax)

# Context managers and async (talking head)

Context managers also support async/await syntax. If you want to learn more about async (concurrent) operations in Python, check out [this] video.

Here's a simple example of an asynchronous context manager taken from the Python documentation:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connection():
    conn = await acquire_db_connection()
    try:
        yield conn
    finally:
        await release_db_connection(conn)

async def get_all_users():
    async with get_connection() as conn:
        return conn.query('SELECT ...')
```

# Context managers + async example (using aiosqlite, screencast)

# When to (not) use context managers

The main reason to use context managers is to help allocate and cleanup resources. This is helpful for example if you want to open a file, a database connection, or a network connection. If an error occurs, the context manager mechanism will automatically clean up the resource.

This also means that if you don't need to cleanup resources, there's no reason to use a context manager. In fact, you shouldn't. Because context managers use the 'with' statement in Python, this also results in an extra code indentation level, and a new scope (because the variable is not accessible outside of the with statement). Nesting with statements introduces more layers and makes things worse:

```python
with open_socket() as s:
    with open_file() as f:
        with open_database() as db:
            do_stuff(s, f, db) # ugh
```

Fortunately, Python allows you to define multiple resources in a single with statement. And since Python 3.10, you can use the parenthesis syntax to split them over multiple lines, like so:

```python
with (
    open_socket() as s,
    open_file() as f,
    open_database() as db
):
    do_stuff(s, f, db) # ugh
```

But of course this only works if you can create the resources at the same time, which isn't possible if there are dependencies between the resources.

I hope you enjoyed this video. If you did, give it a like and consider subscribing to my channel if you want to learn more about software design and development. Thanks for watching, take care, and see you soon.
