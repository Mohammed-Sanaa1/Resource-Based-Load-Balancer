import time
import random
import threading

import master.shared_vars
from master.format_util import tf_presets
from master.format_parser_setup import parse_and_setup_format
tf_preset = parse_and_setup_format()

#mock server class
class MockServer:
    #random modifier constants, used to control how long a task can be. These values are multiplied by the request's weight.
    MIN_RANDOM_TIME_MOD = 0.1
    MAX_RANDOM_TIME_MOD = 0.3

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity        #server's capacity
        self.current_load = 0           #server's current load
        self.requests_handled = []      #logging all handled requests
        self.lock = threading.Lock()    #mutex/semaphore to ensure mutual exclusion

    def get_server_load(self):
        with self.lock:
            load = float(self.current_load)/float(self.capacity)
        #print(f"{self.name}'s load%: {load}")
        return load
    
    #determine whether we can handle the following request or not based on capacity
    def can_handle(self, task_weight):
        with self.lock:
            return self.current_load + task_weight <= self.capacity

    #simulate handle delay according to the task's weight * random modifier
    def handle_request(self, request, task_weight, response_time):
        with self.lock:
            processing_time = task_weight * random.uniform(self.MIN_RANDOM_TIME_MOD, self.MAX_RANDOM_TIME_MOD)
            print(f"{tf_preset.header(f'SERVER {self.name}', tf_preset.server)}: {tf_preset.header('PROCESSING',tf_preset.warning)} request: {tf_preset.header(f'{request}', tf_preset.argument)} (Task weight: {task_weight}, Processing time: {processing_time:.2f}s) {tf_preset.header(f'([current load: {self.current_load}+{task_weight})/{self.capacity}', tf_preset.server_load)}]\n")
            self.current_load += task_weight

        time.sleep(processing_time)

        #log the request when successfully handled and update the load
        with self.lock:
            self.requests_handled.append((request, task_weight, response_time))
            self.current_load -= task_weight
            
            master.shared_vars.threads_remaining -= 1
            print(f"{tf_preset.header(f'SERVER {self.name}', tf_preset.server)}: {tf_preset.header('RELEASED',tf_preset.info)} {task_weight} load(s). {tf_preset.header(f'Current load: {self.current_load}/{self.capacity}',tf_preset.server_load)}\n")
        print(f"{tf_preset.header(f'SERVER {self.name}', tf_preset.server)}: {tf_preset.header('FINISHED',tf_preset.success)} processing request: {request}. {tf_preset.header(f'Current load: {self.current_load}/{self.capacity}',tf_preset.server_load)}\n")

