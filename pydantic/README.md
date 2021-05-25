## About this video

This video is about Pydantic as an extension of the built-in Python dataclasses.

## Video outline

- I did a video about Dataclasses in the past, which is a Python built-in module. Today, I'd like to discuss an alternative called Pydantic. It's not built-in, so if you want to use it you need to install it, but it has a few useful extra possibilities wrt dataclasses.

- Why use Pydantic instead of dataclasses? Pydantic has mostly the same functionality as dataclasses: it defines the equality dunder function as well as the repr and str dunder methods, similar to dataclasses. But the main thing Pydantic adds is extensive support for data validation, conversion and sanitizing. Let's look at an example.

- Give an overview of the sample data.json file

- Read the data from the file and show the contents using a simple print message. Show how you can access the JSON data using dictionary access (which obviously, is not very clean since there is no typechecking whatsoever).

- Now create a Book class using Pydantic's BaseModel (which is similar to a dataclass). Define the various fields, including the optional ones.

- Use the double asterisk syntax to create Book instances from the JSON data. Note that now we have Book instances, we can use the instance variables to access the data, which is much cleaner than accessing JSON data directly.

- Let's add validation for the isbn_10 field. ISBN10's weighted sum of the digits should be divisible by 11.

- You can also add validation on the whole entry using root_validator. We can add the check that a book should have either an ISBN10 or an ISBN13. Because they get a default value of "", we need to do this check on the raw data. To do that, set Pre=True (default, the full validation happens on the processed data)

- There's a Config class you can add to change the behavior or add basic data sanitation:

  - Create an immutable object using allow_mutation = False
  - Automatically convert all str variables to lowercase using anystr_lower = True

- You can easily export data and include or exclude fields usign the .dict() method

- You can create a copy of an object using the .copy() method. Normally, this will create a shallow copy (so no copy of subobjects), but you can set a 'deep' flag to create a deep copy of the object.

- Pydantic has other features as well that I didn't cover in this video, like creating a JSON schema from a model automatically. They also have a BaseSettings class for automatically creating a settings/configuration object using either fields passed as a parameter, or read from the environment. This can be useful if you for example read database connection credentials from environment variables and want a nice way to access them within your code, or override them in a local development environment.
