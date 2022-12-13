import requests

print(requests.put("http://127.0.0.1:8000/update/0?count=-1").json())
print(requests.put("http://127.0.0.1:8000/update/0?price=-1").json())
