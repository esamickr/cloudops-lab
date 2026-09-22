from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
import time


START_TIME = time.time()


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/health":

            response = {
                "status": "healthy",
                "service": "cloudops-lab",
                "version": "1.0"
            }

        elif self.path == "/status":

            response = {
                "hostname": socket.gethostname(),
                "uptime_seconds": int(time.time() - START_TIME),
                "status": "running"
            }

        else:

            response = {
                "message": "CloudOps Lab API"
            }

        data = json.dumps(response).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)


def run_server():

    server = HTTPServer(("0.0.0.0", 8000), Handler)

    print("CloudOps Lab API running on port 8000")

    server.serve_forever()


if __name__ == "__main__":
    run_server()
