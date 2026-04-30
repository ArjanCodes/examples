Start the main API

```
uvicorn main:app --reload --port 8000
```

Start the webhook receiver

```
uvicorn webhook_receiver:app --reload --port 8001
```

## Links

Create a short link

curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://www.arjancodes.com"}'

### Webhook

Create a simple webhook:

```
curl -X POST http://localhost:8000/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://localhost:8001/webhook"
  }'
```

### Events version

Create a webhook:

```
curl -X POST http://localhost:8000/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://localhost:8001/webhook",
    "events": ["link.clicked"]
  }'
```