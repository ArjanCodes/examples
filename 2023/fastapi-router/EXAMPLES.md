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

# Update an item

curl -X PUT -H "Content-Type: application/json" \
 -d '{"description": "Black dual boiler machine"}' \
 http://0.0.0.0:8000/items/1

# Create an automation for item 1

curl -X POST -H "Content-Type: application/json" \
 -d '{"item_id": 1, "code": "print(\"Sending another update notification\")"}' \
 http://0.0.0.0:8000/automations

# Get the automations for item 1

curl -X GET http://0.0.0.0:8000/items/1/automations
