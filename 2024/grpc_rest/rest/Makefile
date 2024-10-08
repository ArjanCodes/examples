# Define the ports and addresses
ENCODING_PORT=8080
ANALYTICS_PORT=8000
CLIENT_PORT=3000

# ----- Running Services -----
.PHONY: start-all start-analytics-service start-client start-encoding-service

# Start all services
start-all: start-analytics-service start-encoding-service start-client
	@echo "All services started."

# Start the Python analytics service (using FastAPI)
start-analytics-service:
	@echo "Starting the Python analytics service..."
	cd ./analytics-service && source .venv/bin/activate && uv run uvicorn main:app --host 0.0.0.0 --port $(ANALYTICS_PORT) --reload

# Start the Go encoding service (REST API)
start-encoding-service:
	@echo "Starting Go encoding service on port $(ENCODING_PORT)..."
	cd ./encoding-service && go run main.go

# Start the React client
start-client:
	@echo "Starting the client service on port $(CLIENT_PORT)..."
	cd ./grpc-web-client && npm start

# ----- Code Generation -----
.PHONY: generate-all

# Generate code for all services (React, Go, Python)
generate-all:
	@echo "No code generation required for the new REST-based services."
