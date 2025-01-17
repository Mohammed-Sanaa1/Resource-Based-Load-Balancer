# Load Balancer Project

## Overview
The Load Balancer Project is a robust system designed to distribute HTTP requests among multiple backend servers efficiently. The system incorporates Flask-based load balancer and backend servers, with additional functionalities for stress testing and simulation. The goal is to ensure high availability, efficient resource utilization, and reliable performance under varying traffic conditions.

---

## Repository Structure

```
.
├── benchmark             # Benchmark file summarizing project results
├── HTTP Server Implementation
│   ├── HTTP-server-RB    # Resource-Based load balancer and servers
│   ├── HTTP-server-RR    # Round-Robin load balancer and servers
│   └── HTTP Client Tests # Test scripts for validating load balancer functionality
├── Stress Testing
│   ├── LB_RB_V5.py       # Load balancer script
│   ├── nodes             # Server nodes
│   ├── stress_test.py    # Stress testing script
│   └── output_fig        # Results visualizations (generated)
├── Simulator
│   ├── master            # Load balancer logic scripts
│   └── test*.py          # Test cases
└── README.md
```

---

## Key Features
- **Load Balancer Implementation:**
  - Supports multiple algorithms: Resource-Based (RB), Round-Robin (RR).
  - Periodic health monitoring to route requests to the least utilized healthy server.
  - Fail-safe mechanisms to handle unavailable servers.
- **Backend Servers:**
  - Flask-based servers providing health and utilization metrics.
  - Efficient resource monitoring using `psutil`.
- **Stress Testing:**
  - Tests load balancer efficiency under sine, square, and polynomial wave traffic patterns.
  - Visualizes results with graphs showing successful vs dropped requests, error rates, and response times.
- **Simulation:**
  - Automated tests for verifying load balancer functionality across edge cases.

---

## Setup and Usage

### Prerequisites
- Python 3.8+
- Required Libraries:
  - Flask, psutil, numpy, pandas, matplotlib, tkinter

### Running the Load Balancer
1. Navigate to the `HTTP Server Implementation` folder.
2. Start backend servers:
   ```bash
   python HTTP-server-RB/server1.py
   python HTTP-server-RB/server2.py
   ```
3. Run the load balancer:
   ```bash
   python HTTP-server-RB/LB_RB.py
   ```
4. Test the load balancer using `HTTP Client Tests` scripts.

### Running Stress Tests
1. Navigate to the `Stress Testing` folder.
2. Start backend servers:
   ```bash
   python nodes/server1.py
   python nodes/server2.py
   ```
3. Start the load balancer:
   ```bash
   python LB_RB_V5.py
   ```
4. Run the stress testing script:
   ```bash
   python stress_test.py
   ```
   Results will be saved in the `output_fig` and `output_csv` folders.

### Running Simulations
1. Navigate to the `Simulator` folder.
2. Run individual test cases:
   ```bash
   python test01.py
   ```
   Add `--pretty` for color-coded logs.

---

## Benchmark Analysis
The project was benchmarked using:
- **Sine Waves:** Demonstrated stability and high performance.
- **Sudden Waves:** Highlighted limitations in handling traffic spikes.
- **Polynomial Waves:** Showed acceptable performance until a critical breaking point.

---

## References
- [Square Wave](https://www.wikiwand.com/en/articles/Square_wave)
- [Sine Wave](https://www.wikiwand.com/en/articles/Sine_wave)

---
