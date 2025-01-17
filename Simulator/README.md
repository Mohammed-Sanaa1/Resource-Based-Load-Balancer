# Simulation with Test Files and Scripts.

## Overview
This branch is dedicated to all the test files and scripts that support the first milestone of the project. It contains automated test scripts that verifies the functionality and integrity of the simulation.

The tests were designed to test edge cases and all conditions the load distributer might encouter.

A detailed overview of each test, alongside their inputs and expected outputs, are written as a header comment above each script.

## Usage
### Running tests
Execute the test file of each case to run it separately:
```
[python/python3] [TESTFILE] [-p/--pretty]
```
The ```--pretty``` argument enables color coding for better log readibility. The decision to make it an optional feature was made to support non-xterm compatible terminals.

## Tests
1. **Basic Functionality Test**: Check if requests are distributed evenly in a round-robin fashion without exceeding the server's capacity.
2. **Overloaded Server Test**: Test if the load balancer skips a server that cannot handle the current request and moves to the next available server.
3. **All Servers Overloaded Test**: Validate how the system responds when all servers are overloaded.
4. **Server Load Release Test**: Ensure that after a server handles a request, it releases the load correctly, making space for new requests.

5. **Edge Case: No Servers Available**: Check how the system behaves when no servers are available at all.
6. **Edge Case: Rapid Fire Requests**: Simulate rapid requests to ensure that the balancer can handle high-frequency traffic without breaking.
7. **Edge Case: Uneven Server Capacities:** Ensure that servers with uneven capacities distribute requests based on their available load.


## Structure
```
.
├── master  #contains the load distributer's main functionality scripts
│   ├── __init__.py         #allows the test files to call scripts in this directory as packages.
│   ├── format_util.py      #Classes for formatting the logs
│   ├── load_balancer.py    #Load balancer class and methods
│   ├── macros.py           #Macros for the return codes for requests handling status
│   └── mock_server.py      #Server node class and methods
├── README.md
├── test cases.txt          #Plain text file that contains the initial tests' plans.
├── test01.py
├── test02.py
├── test03.py
├── test04.py
├── test05.py
├── test06.py
└── test07.py
```

A test summary will be printed at the end of each test along with the logs, showcasing various stats regarding the status of handling each request:
1. **Flawless requests** is reserved for tasks that were handled successfully from the first call (no cycling was needed).
2. **Redirected requests** indicates requests that were successfully handled, but required cycling via the Round-Robin approach.
3. **Dropped requests** status is reserved for requests that were dropped (loss) due to load overflow
4. **Errors** are for miscellaneous errors that were encoutered during request handling.
