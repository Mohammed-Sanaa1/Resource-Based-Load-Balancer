from flask import Flask, redirect, jsonify
import itertools
import requests
import logging

app = Flask(__name__)

# Define the backend servers
servers = [
    {"url": "http://127.0.0.1:5001", "healthy": True},
    {"url": "http://127.0.0.1:5002", "healthy": True},
]

# Create a round-robin iterator over healthy servers
def get_healthy_servers():
    return itertools.cycle([server for server in servers if server["healthy"]])

server_iterator = get_healthy_servers()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Timeout settings (in seconds)
HEALTH_CHECK_TIMEOUT = 2
FORWARD_REQUEST_TIMEOUT = 5

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({"status": "ok", "healthy_servers": [s["url"] for s in servers if s["healthy"]]}), 200

# Health check logic to monitor servers periodically
def check_server_health():
    for server in servers:
        try:
            response = requests.get(f"{server['url']}/", timeout=HEALTH_CHECK_TIMEOUT)
            server["healthy"] = response.status_code == 200
        except requests.RequestException:
            server["healthy"] = False
    global server_iterator
    server_iterator = get_healthy_servers()

# Forward requests to the backend servers
@app.route('/')
def load_balancer():
    # Perform health checks before redirecting
    check_server_health()

    # Find the next healthy server
    for _ in range(len(servers)):
        try:
            target_server = next(server_iterator)["url"]
            logging.info(f"Redirecting to {target_server}")
            # Redirect to the healthy server
            response = requests.get(target_server, timeout=FORWARD_REQUEST_TIMEOUT)
            return response.text, response.status_code
        except StopIteration:
            # No healthy servers available
            logging.error("No healthy servers available!")
            return "Service Unavailable", 503
        except requests.RequestException as e:
            logging.warning(f"Failed to reach server {target_server}: {e}")
            continue

    # If no healthy servers respond
    return "All servers are down!", 503

if __name__ == '__main__':
    app.run(port=5000, debug=True)
