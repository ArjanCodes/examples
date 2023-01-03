import requests

# These requests work:
print(requests.get("http://127.0.0.1:8000/items?count=20").json())
print(requests.get("http://127.0.0.1:8000/items?category=tools").json())


# This request fails because 'ingredient' is not a valid category, as defined in the Category enum:
print(requests.get("http://127.0.0.1:8000/items?category=ingredient").json())


# These request fail because count has to be an integer:

# Here, validation occurs because of the specified type hints on the endpoint.
print(requests.get("http://127.0.0.1:8000/items/?count=Hello").json())

# And here, because of Pydantic.
print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={"name": "Screwdriver", "price": 3.99, "count": 'Hello', "id": 4},
    ).json()
)


