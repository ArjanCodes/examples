import http.server
import os
import socketserver
import webbrowser


class HTMLViewer:
    def __init__(self, filename: str, port: int = 8000) -> None:
        self.filename = filename
        self.port = port
        self._server: socketserver.TCPServer | None = None

    def _open_browser(self) -> None:
        url = f"http://localhost:{self.port}/{self.filename}"
        webbrowser.open(url)

    def _serve(self) -> None:
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            self._server = httpd
            self._open_browser()
            print(f"Serving '{self.filename}' at http://localhost:{self.port}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received. Shutting down server...")
                httpd.shutdown()
                httpd.server_close()

    def start(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(self.filename)))
        self._serve()
