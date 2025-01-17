import numpy as np
import time

from wave_functions import sine_wave_function, sudden_waves_function, polynomial_function
from send_requests import send_requests
import requests
import time

#Set the duration of each wave test here. The delay between each wave also increases with this value
DURATION = 15
#DEBUG: determine the the values of the array here, use this block as a reference to test the array of requests for each wave function 
# array_of_requests_sinewave = []
# array_of_requests_suddenwave = []
# array_of_requests_polynomialwave = []

# for i in range(DURATION):
#    array_of_requests_sinewave.append(sine_wave_function(current_time=i,baseline=350, frequency=0.1, amplitude=100))
#    array_of_requests_suddenwave.append(sudden_waves_function(current_time=i, amplitude=500, baseline=250, frequency=9))
#    array_of_requests_polynomialwave.append(polynomial_function(current_time=i, amplitude=27, baseline=250, time_normalizer=DURATION))

# print(f"sinewave:\t{array_of_requests_sinewave}")
# print(f"suddenwave:\t{array_of_requests_suddenwave}")
# print(f"polynomialwave:\t{array_of_requests_polynomialwave}")

def process_stats(array_of_array_of_dicts):
    #arrays that will hold the final-displayed values
    operation_times_array = []
    requests_sent_array = []
    error_rate_array = []
    mean_response_time_array = []
    peak_response_time_array = []
    successful_requests_array = []
    failed_requests_array = []
    
    for request_stats in array_of_array_of_dicts:
        #temporarily hold the subarray values of each property
        operation_times_subarray = []
        requests_sent_subarray = []
        error_rate_subarray = []
        mean_response_time_subarray = []
        peak_response_time_subarray = []
        successful_requests_subarray = []
        failed_requests_subarray = []
        
        #here we collect the subarray values
        for dictionary in request_stats:
            operation_times_subarray.append(dictionary['total_time'])
            requests_sent_subarray.append(dictionary['requests_sent'])
            error_rate_subarray.append(dictionary['error_rate'])
            mean_response_time_subarray.append(dictionary['mean_response_time'])
            peak_response_time_subarray.append(dictionary['peak_response_time'])
            successful_requests_subarray.append(dictionary['successful_requests'])
            failed_requests_subarray.append(dictionary['failed_requests'])
        
        #perform operations on the subarrays and return a singular value
        #the operation depends on the property and the most important value out of it
        #eg. for error rate, we return the maximum error rate out of all working threads, for mean response time, we return the mean response time of all working threads
        operation_times_array.append(round(float(np.array(operation_times_subarray).max()),5))
        requests_sent_array.append(int(np.array(requests_sent_subarray).sum()))
        error_rate_array.append(round(float(np.array(error_rate_subarray).max()),5))
        mean_response_time_array.append(round(float(np.array(mean_response_time_subarray).mean()),5))
        peak_response_time_array.append(round(float(np.array(peak_response_time_subarray).max()),5))
        successful_requests_array.append(int(np.array(successful_requests_subarray).sum()))
        failed_requests_array.append(int(np.array(failed_requests_subarray).sum()))
            
    return {
            "total_operation_time":operation_times_array,
            "total_requests_sent":requests_sent_array,
            "error_rate":error_rate_array,
            "mean_response_time":mean_response_time_array,
            "peak_response_time":peak_response_time_array,
            "successful_requests": successful_requests_array,
            "failed_requests": failed_requests_array
    }
        
#prints the dictionaries returned from the send_requests() function
def print_stats(dictionary_stat):

        
    #display the results
    print("==============")
    print(f"total operation time:\t{dictionary_stat['total_operation_time']}\n\n")
    
    print(f"total requests sent:\t{dictionary_stat['total_requests_sent']}\n")
    print(f"successful requests:\t{dictionary_stat['successful_requests']}\n")
    print(f"failed requests:\t{dictionary_stat['failed_requests']}\n")
    print(f"error rate:\t\t{dictionary_stat['error_rate']}\n\n")
    
    print(f"mean response time:\t{dictionary_stat['mean_response_time']}\n")
    print(f"peak response time:\t{dictionary_stat['peak_response_time']}\n")
    print("==============\n")

def create_dataframe(processed_data, export_as_csv=False, filename="data.csv"):
    import pandas as pd
    df = pd.DataFrame({
        'total_operation_time': processed_data['total_operation_time'],
        
        'total_requests_sent': processed_data['total_requests_sent'],
        'successful_requests': processed_data['successful_requests'],
        'failed_requests': processed_data['failed_requests'],
        'error_rate': processed_data['error_rate'],
        
        'mean_response_time': processed_data['mean_response_time'],
        'peak_response_time': processed_data['peak_response_time']
    })
    
    if (export_as_csv):
        pd.DataFrame.to_csv(df, filename)
    return df
########################################################
final_counter = DURATION
########################################################
print(f'Simulating a sinus wave for time={DURATION}')
array_of_requests_sinewave = []
for i in range(DURATION):
    array_of_requests_sinewave.append(sine_wave_function(current_time=i,baseline=350, frequency=0.1, amplitude=100))
print(array_of_requests_sinewave)

array_of_sent_sinewave_requests_stats = []
counter = 0
for reqs in array_of_requests_sinewave:
    array_of_sent_sinewave_requests_stats.append(send_requests(reqs, n_jobs=2))
    counter = counter+1
    print(f'{counter}/{final_counter} ...')
print("DONE ✓")

processed_sinewave_data = process_stats(array_of_sent_sinewave_requests_stats)
print_stats(processed_sinewave_data)

print(f'Sleeping for {4*DURATION} seconds to let the Load balancer rest...\n\n')
time.sleep(4*DURATION)

########################################################
print(f'Simulating a sudden wave for time={DURATION}')
array_of_requests_suddenwave = []
for i in range(DURATION):
    array_of_requests_suddenwave.append(sudden_waves_function(current_time=i, amplitude=500, baseline=250, frequency=9))
print(array_of_requests_suddenwave)

array_of_sent_suddenwave_requests = []
counter = 0
for reqs in array_of_requests_suddenwave:
    array_of_sent_suddenwave_requests.append(send_requests(reqs, n_jobs=4))
    counter = counter+1
    print(f'{counter}/{final_counter} ...')
print("DONE ✓")

processed_suddenwave_data = process_stats(array_of_sent_suddenwave_requests)
print_stats(processed_suddenwave_data)

print(f'Sleeping for {4*DURATION} seconds to let the Load balancer rest...\n\n')
time.sleep(4*DURATION)

########################################################
print(f'Simulating a polynomial wave for time={DURATION}')
array_of_requests_polynomialwave = []
for i in range(DURATION):
    array_of_requests_polynomialwave.append(polynomial_function(current_time=i, amplitude=27, baseline=250, time_normalizer=DURATION))
print(array_of_requests_polynomialwave)

array_of_sent_polynomialwave_requests = []
counter = 0
for reqs in array_of_requests_polynomialwave:
    array_of_sent_polynomialwave_requests.append(send_requests(reqs, n_jobs=4))
    counter = counter+1
    print(f'{counter}/{final_counter} ...')
print("DONE ✓")

processed_polynomial_data = process_stats(array_of_sent_polynomialwave_requests)
print_stats(processed_polynomial_data)

import os
dir_path = './output_csv'
if not os.path.exists(dir_path):
      os.makedirs(dir_path)
    
sinewave_df = create_dataframe(processed_sinewave_data, export_as_csv=True, filename="./output_csv/sinewave_data.csv")
suddenwave_df = create_dataframe(processed_suddenwave_data, export_as_csv=True, filename="./output_csv/suddenwave_data.csv")
polynomial_df = create_dataframe(processed_polynomial_data, export_as_csv=True, filename="./output_csv/polynomial_data.csv")
print('Data exported to "./output_csv" folder.')

from data_plotter import plot_data
plot_data(sinewave_df, name="Sinewave function", save_as_image=True)
plot_data(suddenwave_df, name="Suddenwave function", save_as_image=True)
plot_data(polynomial_df, name="Polynomial function", save_as_image=True)