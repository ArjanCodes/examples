import httpx

response = httpx.get(
    "https://business.arjancodes.com/api/v0/courses/66951fb842a33dd06c85e343"
)
print(response.json())
