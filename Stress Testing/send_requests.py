import time
import requests
import threading
import queue
import numpy as np


REQUEST_URL = "http://127.0.0.1:5000/"

#INTERNAL FUNCTION, used by the parent function below
#This function is single-threaded, please refer to the one below it for multi-threading capability!!
def send_requests_routine(number_of_requests):
    array_of_requests_response = []
    successful_requests = 0
    failed_requests = 0
    
    if number_of_requests <= 0:
        print("No requests to send.")
        return

    interval = 1 / number_of_requests  #time interval between requests in seconds
    time_start = time.time()
    
    for i in range(number_of_requests):
        try:
            #record the start time before sending the request
            request_start = time.time()

            #send the request
            response = requests.get(REQUEST_URL)
            if (response.status_code == 200):
                successful_requests = successful_requests+1
        except:
            failed_requests = failed_requests+1
            
        #record the time taken for the request
        request_duration = time.time() - request_start

        #calculate the remaining time to maintain the desired interval
        remaining_time = interval - request_duration
        array_of_requests_response.append(request_duration)

        #sleep for the remaining time if necessary (don't sleep after the last request)
        if i < number_of_requests - 1 and remaining_time > 0:
            time.sleep(remaining_time)

    time_end = time.time()
    total_time = time_end - time_start
    #print(f"Total time elapsed: {total_time:.5f}s")
    #print(f"Requests sent: {number_of_requests}")
    return {
        "total_time": round(total_time,5),
        "requests_sent": number_of_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "error_rate": (failed_requests/number_of_requests),
        "mean_response_time": round(float(np.array(array_of_requests_response).mean()),5),
        "peak_response_time": round(float(np.array(array_of_requests_response).max()),5)
    }

#MULTI-THREADED requests function
#If no number of threads were passed, it will only run on a single thread.
def send_requests(number_of_requests, n_jobs=1):
    threads = []
    results = []
    result_queue = queue.Queue()  #to hold results from threads

    def worker():
        result = send_requests_routine(number_of_requests//n_jobs)
        result_queue.put(result)  #put the result in the queue

    #if n_jobs is 1, run in the main thread without creating new threads
    if n_jobs == 1:
        result = send_requests_routine(number_of_requests)
        results.append(result)
        return results

    #create and start threads
    for _ in range(n_jobs):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    #wait for all threads to complete
    for thread in threads:
        thread.join()

    #collect all results from the queue
    while not result_queue.empty():
        results.append(result_queue.get())

    return results