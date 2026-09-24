from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
import time

from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST


START_TIME = time.time()


REQUEST_COUNT = Counter(
    "cloudops_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "cloudops_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        start = time.perf_counter()

        if self.path == "/health":

            response = {
                "status": "healthy",
                "service": "cloudops-lab",
                "version": "1.1"
            }

            endpoint = "/health"

        elif self.path == "/status":

            response = {
                "hostname": socket.gethostname(),
                "uptime_seconds": int(time.time() - START_TIME),
                "status": "running"
            }

            endpoint = "/status"

        elif self.path == "/metrics":

            data = generate_latest()

            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            self.wfile.write(data)

            REQUEST_COUNT.labels(
                method="GET",
                endpoint="/metrics",
                status="200"
            ).inc()

            REQUEST_LATENCY.labels(
                method="GET",
                endpoint="/metrics"
            ).observe(time.perf_counter() - start)

            return

        else:

            response = {
                "message": "CloudOps Lab API"
            }

            endpoint = "/other"

        data = json.dumps(response).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)

        REQUEST_COUNT.labels(
            method="GET",
            endpoint=endpoint,
            status="200"
        ).inc()

        REQUEST_LATENCY.labels(
            method="GET",
            endpoint=endpoint
        ).observe(time.perf_counter() - start)


def run_server():

    server = HTTPServer(("0.0.0.0", 8000), Handler)

    print("CloudOps Lab API running on port 8000")

    server.serve_forever()


if __name__ == "__main__":
    run_server()
