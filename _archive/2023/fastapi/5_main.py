import requests

# These requests will result in an error, since price and count are negative:
print(requests.put("http://127.0.0.1:8000/update/0?count=-1").json())
print(requests.put("http://127.0.0.1:8000/update/0?price=-1").json())

# Similarly, an item_id must not be negative:
print(requests.put("http://127.0.0.1:8000/update/-1").json())

# And name cannot exceed 8 characters:
print(requests.put("http://127.0.0.1:8000/update/0?name=SuperDuperHammer").json())
