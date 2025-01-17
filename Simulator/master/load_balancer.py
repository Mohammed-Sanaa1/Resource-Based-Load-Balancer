import itertools
import threading
import time

import master.shared_vars
from master.mock_server import MockServer
from master.format_util import tf_presets
from master.format_parser_setup import parse_and_setup_format
tf_preset = parse_and_setup_format()

from master.macros import request_status_macros

#UPDATED ROUND ROBIN LOAD BALANCER: added weight consideration
class ResourceBasedBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.server_iter = itertools.cycle(servers)
        self.lock = threading.Lock()

    #main function: cycle and handle the request
    def distribute_request(self, request, task_weight):
        #check for servers' length. Should be cast into a list first to use len() since it's an iterator
        if len(list(self.servers)) == 0:
            print(tf_preset.header('CRITICAL WARNING: No servers were detected!!', tf_preset.danger))
            return request_status_macros.ERROR


        time_start = time.perf_counter()     
        minimum = self.servers[0]   #assume first server is always the minimum.
        for i in self.servers:      #iterate through all servers
            if i.get_server_load() < minimum.get_server_load():
                with self.lock: #make sure the server can handle the weight before assignment
                    if i.current_load + task_weight <= i.capacity:
                        minimum = i
        
        #FAIL STATE
        with self.lock:
            if minimum.current_load + task_weight > minimum.capacity:      #If we did a complete cycle; then no server has met our condition
                print(f"{tf_preset.header('BALANCER', tf_preset.balancer)}: {tf_preset.header('No available server can handle the request due to capacity overload!',tf_preset.danger_blink)}\n")
                return request_status_macros.REQUEST_DROPPED

        server = minimum
        #SERVER IS FOUND: handle the request
        time_end = time.perf_counter()
        time_elapsed = time_end - time_start        ##CALCULATE RESPONSE TIME
        print(f"{tf_preset.header('BALANCER', tf_preset.balancer)}: Distributing request {tf_preset.header(f'{request}', tf_preset.argument)} (Weight: {task_weight}) to {server.name}\n")

        #start a new thread to handle the request on the selected server.
        #this allows the load balancer to continue distributing other requests without waiting for this one to finish.
        threading.Thread(target=server.handle_request, args=(request, task_weight, time_elapsed)).start()
        master.shared_vars.threads_remaining += 1
        
        return request_status_macros.REQUEST_SUCCESS