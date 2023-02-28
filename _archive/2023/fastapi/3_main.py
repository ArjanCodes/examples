import requests

print("Adding an item:")
print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={"name": "Screwdriver", "price": 3.99, "count": 10, "id": 4},
    ).json()
)
print(requests.get("http://127.0.0.1:8000/").json())
print()

print("Updating an item:")
print(requests.put("http://127.0.0.1:8000/update/0?count=9001").json())
print(requests.get("http://127.0.0.1:8000/").json())
print()

print("Deleting an item:")
print(requests.delete("http://127.0.0.1:8000/delete/0").json())
print(requests.get("http://127.0.0.1:8000/").json())
