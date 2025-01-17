# Load Balancer Stress Testing/Data extractor

## Overview
This branch performs a comprehensive stress test on different load-balancing algorithms to evaluate the efficiency and the robusteness of said algorithms under various traffic patterns to measure how they handle high volumes of requests, manage server utilization and ensure minimal dropped requests.

The results of the stress tests are visualized through detailed graphs and plots, showcasing:
* Number of requests send vs Error rate
* Sucessful vs Dropped requests over time.
* Response Time / Latency

The test summary's columns are as follows:
1. **total_requests_sent**: Number of requests sent during that second.
2. **successful_requests**: Number of successful requests handled by the Load Balancer.
3. **failed_requests**:     Number of requests the Load Balancer failed to deliver.
4. **error_rate**:          Successful to failed requests' ratio.
5. **mean_response_time**:  Average response time for all requests during that second.
6. **peak_response_time**:  Highest recorded response time for a request on that second.

## Required libraries / dependencies
* numpy
* pandas
* matplotlib
* tkinter
* cpuinfo
* psutil
* flask

## Usage
### 1. Initializing the environment
1. Open 3 different terminals
2. Run Each server node on a different terminal:
```
python nodes/server1.py
```
```
python nodes/server2.py
```

3. Launch the Load balancer on the third terminal:
```
python LB_RB_V5.py
```

### 2. Running the test
1. On a new terminal, run the stress testing program `stress_test.py` and wait for it to finish: 
```
python stress_test.py
```

The progress and current steps will be logged to the terminal.

After the test concludes, two folders will be generated, `output_csv` and `output_fig`, containing charts detailing the tests results and visualized graphs of said data, respectively.

> [!IMPORTANT]
> The test performs a significant amount of GET requests. this might cause a port-exhaustion issue. To alleviate this, a timeout between each phase of the test is applied to let the OS clean the ports if needed. The timeout's duration is relative to the test's duration, longer tests constitute longer wait times.

## Folder Structure
```
.
.
├── data_plotter.py     #contains functionalities for plotting the data.
├── LB_RB_V5.py         #Load balancer
├── nodes               #Server nodes' directory
│   ├── server1.py
│   └── server2.py
├── output_csv          #generated directory, contains .csv files for each tests' results
├── output_fig          #generated directory, contains .png images for each tests' results' graph 
│
├── README.md
├── send_requests.py    #Contains methods for sending and processing requests from the server
├── stress_test.py      #Main test driver program.
└── wave_functions.py   #Contains the mathematical models that returns the number of requests corresponding each wave function.
```
