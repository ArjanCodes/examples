## Introduction

- Perhaps some joke about how FastAPI is the blazingly fastest of all the blazingly fast API frameworks out there, or is that too on-the-nose?

FastAPI advantages:

- easy to learn
- fast to write and fast in performance
- automatic conversion to JSON → you can use native python types like dicts in your code
- automatic data validation in a pythonic way using type hints
- automatic documentation for your API

(disadvantages for completeness:

- People claim it is not as scalable, although that is difficult for me to judge
  - The problem seems to lie in the server rather than FastAPI itself.
  - [FastAPI can also be used with gunicorn instead of uvicorn (default) which seems to address this issue)](https://stackoverflow.com/questions/67137350/how-to-deploy-a-scalable-api-using-fastapi)

## Installation

- `pip install "fastapi[all]"` will install fastapi with all optional / default modules
- Alternatively, `pip install fastapi "uvicorn[standard]"` will install a reduced amount of packages

## Creating the app

- Create a simple inventory management system (show example `1_basic_app.py`)
  - Items can be in a local dict for now (this can be later used to demonstrate why a database + ORM is needed → reload server and all changes will be gone)
  - Creating the app is as simple as `app = FastAPI()`
  - Here we also add a simple GET endpoint that returns the data stored in our system.
  - In our Python code we can directly use built-in types, in this case a dictionary. FastAPI automatically handles the conversion to JSON for you.
  - You can run the app by calling: `uvicorn main:app --reload`.
  - You can interact with the API either through your web browser (for simple GET requests) or programmatically e.g. using the requests package in Python (see `1_main.py`)
  - Here we can allude to another way of interacting with the API that we will talk about later in the video (referring to the auto-generated documentation)

## Path and query parameters

- Next, let us add some endpoints for querying our data (see example `2_creating_get_route_query.py`)
- Our first endpoint lets us directly query an Item by its id.
  - We can realize this using a path parameter (denoted by {} in the path)
  - Path parameters will be passed to the decorated function as kwargs, so make sure that the name is the same in the path and the function signature.
- The other endpoint lets us query a selection of items based on their properties: name, price, count, and category.
  - You may have noticed that these parameters do not appear in the endpoint's path.
  - Instead, we are using query parameters in this case. This is a neat way to specify any number of potential arguments for a given endpoint. In a request, you would specify them by giving the endpoint followed by a ? and the query parameters you wish to pass. Vaguely similar to Python’s kwargs but separated by `&` instead of `,`.
  - Example `2_main.py` demonstrates how one could use these endpoints for either querying a specific item with the ID 1 or items with the name “Nails”.

## Routing and requests

- You can use FastAPI to implement all endpoints, not just GET. (see example `3_more_routing.py`)
- Here we have extended our API to be able to manipulate our data in addition to retrieving it.
- We use POST for creating new data, PUT for modifying existing data, and DELETE for, unsurprisingly, deleting data.
- This is a convention rather than a hard constraint. There is nothing preventing you from manipulating data from GET endpoints. Still, your should definitely stick to this convention unless your goal is to become the #1 unpopular person at your workplace.
- Example `3_main.py` shows how you would use the endpoints we have created to add, modify and delete an item in our inventory management system.
- Notice how the new item is specified in JSON format in the request but is automatically converted by FastAPI into an instance of `Item` and passed to our endpoint function.

## FastAPI advantage #1: simplicity and speed of writing code

- As you can see, creating in API using FastAPI is simple and intuitive. The support for built-in python types removes the necessity of casting variables to and from JSON, which saves you a lot of boilerplate and makes the code much nicer.
- The use of decorators for specifying endpoints is also very intuitive and clean. Although it is not exclusive to FastAPI (Flask does it similarly), I prefer to have methods for the different request types rather than having to specify them as arguments to a generic `route` method.
- Being able to specify query and path parameters in the function signature is a big plus and greatly contributes to keeping to code clean and readable.

## FastAPI advantage #2.1: automatic validation

- But FastAPI provides more than just a nice way to write your API.
- The first big feature I want to talk about in this video is the built-in data validation.
- FastAPI relies on type hints to validate data (see example `4_main.py`). When we provide data that cannot be interpreted as the type we specified in the endpoint’s function signature, FastAPI will return an error message. No manual checks required!
- If we want to limit the choices for string arguments, we can create a regular Python enum and specify it as the type hint for the string parameter. FastAPI will ensure that only valid enum entries get through to the endpoint’s function.
- This concept even extends to custom data structures, such as our `Item` class. Here we have explicitly inherited from Pydantic’s `BaseModel` but it would’ve also worked with a regular `@dataclass`
- Under the hood FastAPI delegates all validation to Pydanti, so you know that it is fast and reliable.
- You get all this by simply specifying type hints in your code. Nice!

## FastAPI advantage #2.2: automatic validation beyond types

- You can put further restrictions on your path and query arguments beyond checking their type.
- For this, you can set the default values of the corresponding parameters to instances of the `Path` and `Query` classes. (see example `5_validation_with_Query_and_Path.py`)
- In this example, we have placed restrictions on the path and query parameters of our `update` endpoint:
  - FastAPI will now ensure that `item_id`, `price`, and `count` are non-negative.
  - Arguments to `name` must now be between 1 and 8 characters long
- Example `5_main.py` showcases the responses we get when supplying invalid arguments.
- FastAPI generates informative error messages that make the restrictions on the arguments transparent to the user.

## FastAPI advantage #3: auto-generated documentation

- The second prominent feature that FastAPI brings to the table is auto-generated interactive documentation of our API
- You can view the Swagger UI by navigating to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) or the ReDoc UI by going to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- This documentation shows all of the endpoints in our API, the data they receive and return, and the responses you might expect from them.
- Additionally, it also shows the Schemas in the API. Notice that our `Item` class and the `Category` enum are already listed there.
- You can flesh out this documentation by providing additional information (see example `6_adding_openapi_documentation.py`), e.g. metadata in the form of title and description for the app and individual query and path parameters.
- You can also add responses to the endpoint documentation that FastAPI cannot infer directly, such as a 404 response, when an item is not found.
