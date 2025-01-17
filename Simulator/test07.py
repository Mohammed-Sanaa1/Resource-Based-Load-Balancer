'''
7. Edge Case: Uneven Server Capacities
Test Case: Ensure that servers with uneven capacities distribute requests based on their available load.

Input:
    Servers:
    S1=5
    S2=15
    S3=30
    
    Requests:
    10 requests with weight = 3 each.
'''
from master.load_balancer import ResourceBasedBalancer
from master.mock_server import MockServer
from master.macros import request_status_macros
import random
import time

from master.format_parser_setup import parse_and_setup_format
tf_preset = parse_and_setup_format()

#create mock servers with different capacities
mock_servers = [
    MockServer("S1", capacity=5),
    MockServer("S2", capacity=15),
    MockServer("S3", capacity=30)
]

#initialize the load balancer with the above array
load_balancer = ResourceBasedBalancer(mock_servers)


#TESTING
flawless_requests = 0
redirected_requests = 0
errors = 0
dropped_requests = 0

for i in range(1, 10):
    result = load_balancer.distribute_request(f'R{i}', 3)
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