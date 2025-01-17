import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

BASE_URL = 'http://127.0.0.1:5000'
NUM_REQUESTS = 1000  # Number of requests to send
NUM_THREADS = 20   # Number of parallel threads
REQUEST_TIMEOUT = 0.2  # Timeout for each request in seconds

def send_request(results, endpoint, lock):
    try:
        start_time = time.time()
        response = requests.get(BASE_URL + endpoint, timeout=REQUEST_TIMEOUT) #, timeout=REQUEST_TIMEOUT
        end_time = time.time()

        with lock:
            results['total_requests'] += 1
            results['response_times'].append(end_time - start_time)

            if response.status_code == 200:
                results['successes'] += 1
            else:
                results['drops'] += 1
    except requests.exceptions.RequestException as e:
        with lock:
            results['drops'] += 1
        print(f"Request failed: {e}")

def test_root_endpoint():
    endpoint = '/'
    results = {
        'total_requests': 0,
        'successes': 0,
        'drops': 0,
        'response_times': []
    }
    lock = Lock()

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        start_time_T = time.time()
        futures = [executor.submit(send_request, results, endpoint, lock) for _ in range(NUM_REQUESTS)]
        for future in as_completed(futures):
            try:
                future.result()  # Wait for each thread to complete and handle exceptions
            except Exception as e:
                print(f"An error occurred: {e}")
        end_time_T = time.time()

    print(f"Total requests: {results['total_requests']}")
    print(f"Successful requests: {results['successes']}")
    print(f"Dropped requests: {results['drops']}")
    if results['response_times']:
        print(f"Average response time: {sum(results['response_times']) / len(results['response_times']):.4f} seconds")
    else:
        print("No successful requests to calculate average response time.")
    
    print(f"TIME: {(end_time_T-start_time_T):.3f}")

if __name__ == "__main__":
    test_root_endpoint()
