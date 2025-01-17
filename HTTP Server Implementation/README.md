# HTTP Server Implementation

## Overview
This folder contains implementations of two load balancing algorithms:
1. **Resource-Based (RB):** Routes requests based on server utilization metrics.
2. **Round-Robin (RR):** Sequentially assigns requests to servers.

Additionally, it includes test scripts to validate the functionality of the load balancer.

---

## Folder Structure
```
HTTP Server Implementation
├── HTTP-server-RB        # Resource-Based implementation
│   ├── LB_RB.py          # Load balancer script
│   ├── server1.py        # Backend server 1
│   └── server2.py        # Backend server 2
├── HTTP-server-RR        # Round-Robin implementation
│   ├── LB_RR.py          # Load balancer script
│   ├── server1.py        # Backend server 1
│   └── server2.py        # Backend server 2
└── HTTP Client Tests     # Test scripts for load balancer validation
    ├── single_thread_tester.py # Single-threaded client test 
    ├── multithreading_tester.py # Multi-threaded client test 
    └── simple_client.py # Simple client to test server responses
```

---

## Key Features
- **Load Balancers:**
  - RB: Dynamically routes requests to the least utilized healthy server.
  - RR: Distributes requests in a fixed sequential order.
- **Backend Servers:**
  - Flask-based servers with health monitoring and utilization reporting.
- **Client Tests:**
  - **single_thread_tester.py:** Tests the server's performance using a single-threaded client sending 1000 requests sequentially.
  - **multithreading_tester.py:** Evaluates the server's ability to handle concurrent requests with up to 20 threads.
  - **simple_client.py:** A basic script to verify server functionality by sending a single request.

---

## Setup and Usage

### Prerequisites
- Python 3.8+
- Required Libraries:
  - Flask, psutil

### Running the Load Balancer
1. Start backend servers:
   ```bash
   python HTTP-server-RB/server1.py
   python HTTP-server-RB/server2.py
   ```
2. Run the load balancer:
   ```bash
   python HTTP-server-RB/LB_RB.py
   ```

For Round-Robin, repeat the above steps with the `HTTP-server-RR` folder.

### Running Tests
1. Navigate to the `HTTP Client Tests` folder.
2. Run test scripts:
   ```bash
   python single_thread_tester.py
   ```

---

## Notes
- The Resource-Based algorithm demonstrated superior performance in benchmarks.
- Logs provide detailed insights into server health and request routing.
- Test scripts include output for total requests, successful requests, dropped requests, average response times, and total test time.

---

