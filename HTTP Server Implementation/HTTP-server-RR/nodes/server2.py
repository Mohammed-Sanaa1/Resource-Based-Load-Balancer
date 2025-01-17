from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from server2!'

@app.route('/utilization')
def utilization():
    # Gather system utilization metrics
    utilization_data = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        # Add more metrics as needed
    }
    return jsonify(utilization_data), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True, threaded=False)
