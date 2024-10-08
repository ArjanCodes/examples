import grpc
import authenticator_pb2
import authenticator_pb2_grpc

def run(uuid):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = authenticator_pb2_grpc.AuthenticatorStub(channel)
        request = authenticator_pb2.AuthenticationRequest(uuid=uuid)
        response = stub.Authenticate(request)
    print(f"Result: {response.result}")

if __name__ == '__main__':
    # Get user Input 
    uuid = "9f4e62ce-7b8e-4205-83d5-9800b528a1c8"
    run(uuid)