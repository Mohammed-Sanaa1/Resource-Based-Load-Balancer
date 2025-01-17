from flask import Flask, jsonify
import psutil

app = Flask(__name__)

def calculate_utilization():
    cpu_percent = psutil.cpu_percent(interval=None)
    memory_percent = psutil.virtual_memory().percent
    
    # Define weights for CPU and memory utilization
    cpu_weight = 0.7
    memory_weight = 0.3
    
    # Calculate weighted utilization
    utilization = (cpu_percent * cpu_weight) + (memory_percent * memory_weight)
    return round(utilization, 3)


@app.route('/')
def hello_world():
    return 'Hello from server1!'


@app.route('/health')
def health():
    utilization_value = calculate_utilization()
    return jsonify({"status": "ok", "utilization": utilization_value}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True, threaded=True)



# @app.route('/utilization')
# def utilization():
#     utilization_value = calculate_utilization()
#     utilization_data = {
#         "utilization": utilization_value
#     }
#     return jsonify(utilization_data), 200