from flask import Flask
import socket
import time

app = Flask(__name__)

start_time = time.time()

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "cloudops-lab",
        "version": "1.0"
    }

@app.route("/status")
def status():
    return {
        "hostname": socket.gethostname(),
        "uptime_seconds": round(time.time() - start_time, 2)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
