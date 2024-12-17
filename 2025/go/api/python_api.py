import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class SimpleHandler(BaseHTTPRequestHandler):
    # Handle GET requests
    def do_GET(self) -> None:
        # Parse the URL and query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path != "/hello":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"error": "Not Found"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # Get the 'name' parameter from the query string, default to 'World'
        name = query_params.get("name", ["World"])[0]
        response = {"message": f"Hello, {name}!"}

        # Send HTTP headers
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        # Send the JSON response
        self.wfile.write(json.dumps(response).encode("utf-8"))


# Start the HTTP server
def main() -> None:
    port = 8080
    httpd = HTTPServer(("", port), SimpleHandler)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
