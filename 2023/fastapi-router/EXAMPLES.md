# Start the server

```bash
uvicorn main:app --reload
```

# Create an item

curl -X POST -H "Content-Type: application/json" \
 -d '{"name": "Espresso machine", "description": "Silver dual boiler machine"}' \
 http://0.0.0.0:8000/items

# Read an item

curl -X GET http://0.0.0.0:8000/items/1
