import grpc
from concurrent import futures
import authenticator_pb2
import authenticator_pb2_grpc

class AuthenticatorServicer(authenticator_pb2_grpc.AuthenticatorServicer):
    def authenticate(self, request, context):
        # Implement the authentication logic here
        if request.uuid == "9f4e62ce-7b8e-4205-83d5-9800b528a1c8":
            return authenticator_pb2.AuthenticationResponse(
                message="Authenticated successfully", valid=True
            )
        else:
            return authenticator_pb2.AuthenticationResponse(
                message="Invalid UUID", valid=False
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    authenticator_pb2_grpc.add_AuthenticatorServicer_to_server(AuthenticatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
