'''
4. Server Load Release Test:
Test Case: Ensure that after a server handles a request, it releases the load correctly, making space for new requests.

Input:
    Servers:
    S1=5
    S2=5
    
    Requests:
    R1=5
    R2=5
    NOTE:We will simulate a delay in requests to give the servers time to release the load, then send two more requests to those servers
    R3=5
    R4=5
'''

from master.load_balancer import ResourceBasedBalancer
from master.mock_server import MockServer
from master.macros import request_status_macros
import time

from master.format_parser_setup import parse_and_setup_format
tf_preset = parse_and_setup_format()

#create mock servers with different capacities
mock_servers = [
    MockServer("S1", capacity=5),
    MockServer("S2", capacity=5)
]

#initialize the load balancer with the above array
load_balancer = ResourceBasedBalancer(mock_servers)

#initialize tasks with specified weights
tasks_first_batch = [
    ("R1", 5),
    ("R2", 5),
]
tasks_second_batch = [
    ("R3", 5),
    ("R4", 5),
]

#TESTING
flawless_requests = 0
redirected_requests = 0
errors = 0
dropped_requests = 0

for request, task_weight in tasks_first_batch:
    result = load_balancer.distribute_request(request, task_weight)
    if result == request_status_macros.REQUEST_SUCCESS:
        flawless_requests +=1
    elif result == request_status_macros.REQUEST_SUCCESS_REDIRECTED:
        redirected_requests+=1
    elif result == request_status_macros.REQUEST_DROPPED:
        dropped_requests+=1
    elif result == request_status_macros.ERROR:
        errors+=1
time.sleep(2)
for request, task_weight in tasks_second_batch:
    result = load_balancer.distribute_request(request, task_weight)
    if result == request_status_macros.REQUEST_SUCCESS:
        flawless_requests +=1
    elif result == request_status_macros.REQUEST_SUCCESS_REDIRECTED:
        redirected_requests+=1
    elif result == request_status_macros.REQUEST_DROPPED:
        dropped_requests+=1
    elif result == request_status_macros.ERROR:
        errors+=1

import master.shared_vars
master.shared_vars.wait_for_all_threads()
time.sleep(0.5)

print(20*'=')
print('TEST SUMMARY:')
print(f"{tf_preset.header('Flawless requests',tf_preset.success)}: {flawless_requests}")
print(f"{tf_preset.header('Redirected requests',tf_preset.warning)}: {redirected_requests}")
print(f"{tf_preset.header('Dropped requests',tf_preset.danger)} (due to overflow): {dropped_requests}")
print(f"{tf_preset.header('Errors',tf_preset.danger)}: {errors}")
print(tf_preset.header('LOAD RELEASES MIGHT FOLLOW SHORTLY.',tf_preset.info))
print(20*'=')

print("Response times:")
for i in mock_servers:
    print(f"server node #{i.name}")
    for j in i.requests_handled:
        print(f"\tRequest #{j[0]}: {round(j[2] * 1_000_000 ,3)} microseconds response time")