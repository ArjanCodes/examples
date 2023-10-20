import httpx

base_url = "https://httpbin.org"

# GET
response = httpx.get(f"{base_url}/get")
print("GET:", response.json())

# POST
data_to_post = {"key": "value"}
response = httpx.post(f"{base_url}/post", json=data_to_post)
print("POST:", response.json())

# PUT
data_to_put = {"key": "updated_value"}
response = httpx.put(f"{base_url}/put", json=data_to_put)
print("PUT:", response.json())

# DELETE
response = httpx.delete(f"{base_url}/delete")
print("DELETE:", response.json())
