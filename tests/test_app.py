import threading
import time
import urllib.request

from http.server import HTTPServer

from app.app import Handler


def start_test_server():
    server = HTTPServer(("127.0.0.1", 0), Handler)

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True
    )

    thread.start()

    time.sleep(0.1)

    return server


def test_health():

    server = start_test_server()

    port = server.server_address[1]

    response = urllib.request.urlopen(
        f"http://127.0.0.1:{port}/health"
    )

    assert response.status == 200

    data = response.read().decode()

    assert '"status": "healthy"' in data
    assert '"service": "cloudops-lab"' in data

    server.shutdown()
