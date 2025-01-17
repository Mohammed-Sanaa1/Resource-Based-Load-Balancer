from flask import Flask, jsonify
import itertools
import requests
import logging
import threading
import time

app = Flask(__name__)

# Define the backend servers
servers = [
    {"url": "http://127.0.0.1:5001", "healthy": True, "utilization": 0},
    {"url": "http://127.0.0.1:5002", "healthy": True, "utilization": 0},
]

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Timeout settings (in seconds)
HEALTH_CHECK_TIMEOUT = 2
FORWARD_REQUEST_TIMEOUT = 5

# Health check logic to monitor servers periodically
def check_server_health():
    while True:  # Continuously check server health
        for server in servers:  # Iterate through servers
            try:
                # Send a GET request to the server's health endpoint
                response = requests.get(f"{server['url']}/health", timeout=HEALTH_CHECK_TIMEOUT)
                
                if response.status_code == 200:  # Successful response
                    health_data = response.json()  # Parse JSON response
                    server["healthy"] = True  # Mark server as healthy
                    server["utilization"] = health_data.get("utilization", 100)  # Update utilization
                    logging.info(f"Server {server['url']} is healthy with utilization {server['utilization']}")
                else:  # Unsuccessful response
                    server["healthy"] = False  # Mark server as unhealthy
                    server["utilization"] = 100  # Set utilization to 100%
                    logging.warning(f"Server {server['url']} is unhealthy with response code {response.status_code}")
            except requests.RequestException as e:  # Exception during request
                server["healthy"] = False  # Mark server as unhealthy
                server["utilization"] = 100  # Set utilization to 100%
                logging.error(f"Failed to reach server {server['url']}: {e}")
        
        # Log list of healthy servers
        logging.info(f"Healthy servers: {', '.join([s['url'] for s in servers if s['healthy']])}")
        time.sleep(5)  # Wait before next health check



# Start the health check thread
health_check_thread = threading.Thread(target=check_server_health, daemon=True)
health_check_thread.start()

# Health check endpoint
@app.route('/health')
def health():
    # healthy_servers = [s["url"] for s in servers if s["healthy"]]
    # return jsonify({"status": "ok", "healthy_servers": healthy_servers}), 200
    return jsonify(servers)

# Forward requests to the backend servers
@app.route('/')
def load_balancer():
    # Find the least utilized healthy server
    healthy_servers = [s for s in servers if s["healthy"]]
    if not healthy_servers:
        logging.error("No healthy servers available!")
        return "Service Unavailable", 503

    least_utilized_server = min(healthy_servers, key=lambda s: s["utilization"])
    target_server = least_utilized_server["url"]
    logging.info(f"Redirecting to {target_server}")

    try:
        # Forward the request to the least utilized server
        response = requests.get(target_server, timeout=FORWARD_REQUEST_TIMEOUT)
        return response.text, response.status_code
    except requests.RequestException as e:
        logging.warning(f"Failed to reach server {target_server}: {e}")
        return "Service Unavailable", 503

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
