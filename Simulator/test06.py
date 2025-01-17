'''
6. Edge Case: Rapid Fire Requests
Test Case: Simulate rapid requests to ensure that the balancer can handle high-frequency traffic without breaking.

Input:
    Servers:
    S1=50
    S2=50
    
    Requests:
    Send 100 requests with random weights between 1 and 10.
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
    MockServer("S1", capacity=50),
    MockServer("S2", capacity=50),
]

#initialize the load balancer with the above array
load_balancer = ResourceBasedBalancer(mock_servers)


#TESTING
flawless_requests = 0
redirected_requests = 0
errors = 0
dropped_requests = 0

for i in range(0, 100):
    time.sleep(0.1)
    result = load_balancer.distribute_request(f'R{i}', random.randint(1, 10))
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