import requests
import time

BASE_URL = 'http://127.0.0.1:5000'
REQUEST_TIMEOUT = 0.1  # Timeout for each request in seconds
NUM_REQUESTS = 1000  # Number of requests to send

def test_root_endpoint():
    endpoint = '/'
    results = {
        'total_requests': 0,
        'successes': 0,
        'drops': 0,
        'response_times': []
    }

    start_time_T = time.time()
    for _ in range(NUM_REQUESTS):  # Send 10 requests to the root endpoint
        try:
            start_time = time.time()
            response = requests.get(BASE_URL + endpoint)
            end_time = time.time()

            results['total_requests'] += 1
            results['response_times'].append(end_time - start_time)

            if response.status_code == 200:
                results['successes'] += 1
            else:
                results['drops'] += 1
        except requests.exceptions.RequestException as e:
            results['drops'] += 1
            print(f"Request failed: {e}")

    end_time_T = time.time()

    print(f"Total requests: {results['total_requests']}")
    print(f"Successful requests: {results['successes']}")
    print(f"Dropped requests: {results['drops']}")
    if results['response_times']:
        print(f"Average response time: {sum(results['response_times']) / len(results['response_times']):.4f} seconds")
        print(f"Total response time: {sum(results['response_times']):.3f}")
    else:
        print("No successful requests to calculate average response time.")
    
    print(f"TIME: {(end_time_T-start_time_T):.3f}")

if __name__ == "__main__":
    test_root_endpoint()



