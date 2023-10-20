import requests

base_url = "https://httpbin.org"

# GET
response = requests.get(f"{base_url}/get")
print("GET:", response.json())

# POST
data_to_post = {"key": "value"}
response = requests.post(f"{base_url}/post", json=data_to_post)
print("POST:", response.json())

# PUT
data_to_put = {"key": "updated_value"}
response = requests.put(f"{base_url}/put", json=data_to_put)
print("PUT:", response.json())

# DELETE
response = requests.delete(f"{base_url}/delete")
print("DELETE:", response.json())
