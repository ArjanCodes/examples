# Define the ports and addresses
GRPC_PORT=50051
PROXY_PORT=8080
GRPC_ADDR=localhost:$(GRPC_PORT)

# ----- Code Generation -----
.PHONY: generate-all generate-analytics-service-code generate-encoding-service-code generate-client-service-code

# Generate code for all services
generate-all: generate-analytics-service-code generate-encoding-service-code generate-client-service-code generate-analytics-service-code
	@echo "Generated code for all services."

# Generate code for the Encoding service (Go)
generate-encoding-service-code:
	@echo "Generating code for the Encoding service..."
	protoc --proto_path=./proto --go_out=./encoding-service/pkg/grpc/generated --go-grpc_out=./encoding-service/pkg/grpc/generated ./proto/encoding.proto


# Generate code for the Analytics service (Python)
generate-analytics-service-code:
	@echo "Generating code for the Analytics service..."
	python -m grpc_tools.protoc -I./proto --python_out=./analytics-service/analytics --grpc_python_out=./analytics-service/analytics ./proto/analytics.proto

# Generate code for the React client service (gRPC-Web)
generate-client-service-code:
	@echo "Generating gRPC-Web code for the client service..."
	protoc -I=./proto --js_out=import_style=commonjs:./grpc-web-client/src/grpc --grpc-web_out=import_style=commonjs,mode=grpcwebtext:./grpc-web-client/src/grpc ./proto/encoding.proto
	protoc -I=./proto --js_out=import_style=commonjs:./grpc-web-client/src/grpc --grpc-web_out=import_style=commonjs,mode=grpcwebtext:./grpc-web-client/src/grpc ./proto/analytics.proto

# ----- Running Services -----
.PHONY: start-all start-analytics-service start-client run-grpc-service run-grpc-web-proxy

# Start the Python analytics service
start-analytics-service:
	@echo "Starting the Python analytics service..."
	cd ./analytics-service && source .venv/bin/activate && python ./main.py

# Start the React client
start-client:
	@echo "Starting the client service..."
	cd ./grpc-web-client && npm start

# Run the Go gRPC service (backend)
start-encoding-service:
	@echo "Starting Go gRPC service on port $(GRPC_PORT)..."
	cd ./encoding-service && go run main.go

# Run the gRPC-Web proxy
start-grpc-web-proxy:
	@echo "Starting gRPC-Web proxy on port $(PROXY_PORT)..."
	grpcwebproxy --backend_addr=$(GRPC_ADDR) --run_http_server=true --run_tls_server=false --server_http_debug_port=$(PROXY_PORT) --allow_all_origins
