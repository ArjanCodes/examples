# Create an item

curl -X POST -H "Content-Type: application/json" \
 -d '{"name": "Espresso machine", "description": "Silver dual boiler machine"}' \
 http://0.0.0.0:8000/items
