# SDN-based Application-Aware Adaptive Load Balancer
This project is a Master's thesis artefact demonstrating an intelligent, adaptive load balancing system built on Software-Defined Networking (SDN) principles. The system uses a centralized Ryu controller to dynamically manage network traffic based on the real-time CPU load of backend application servers, complete with a live web-based monitoring dashboard.
### Features
**Centralized SDN Control**: Uses the Ryu framework to manage an OpenFlow-enabled virtual switch.

**Application-Aware Monitoring**: The controller actively polls backend servers via a REST API to get real-time CPU utilization.

**Adaptive Traffic Steering**: Automatically removes overloaded or unresponsive servers from the active pool and re-integrates them upon recovery.

**Live Visual Dashboard**: A Flask-based web interface provides a real-time, color-coded view of each server's health and CPU load.

**Interactive Control**: The dashboard includes buttons to manually apply CPU load to any server for demonstration and testing purposes.

**Virtual Testbed**: Built on Mininet for easy, reproducible network emulation.
### Architecture
The system is composed of four main components:
 1. **SDN Controller (controller.py)**: The brain of the system. A Ryu application that runs the L2 switching logic, the adaptive load balancing algorithm, and the Flask web server for the dashboard.
 2. **Network Topology (topology.py)**: A Mininet script that defines the virtual network, including a client, multiple servers, and an OpenFlow switch.
 3. **Application Server (server_app.py)**: A smart Flask application that runs on each backend server. It serves content and exposes /metrics and /load API endpoints.
 4. **Frontend Dashboard (templates/index.html)**: A single-page web application that visualizes the real-time status of the server pool.

[Check the architecture diagram at imgur](https://imgur.com/a/IA1ukTJ)

### Prerequisites
This project is designed to run in a Linux environment. An Ubuntu 22.04 LTS virtual machine is recommended.
 - Python 3.8+
 - Mininet
 - Open vSwitch
 - Ryu SDN Framework
 - Python libraries: flask, psutil, requests, werkzeug

## Quick Setup
 1. ### Clone the repository:
  ```
   git clone https://github.com/ismaelmiah/Load-Balancer-Using-SDN.git
   cd Load-Balancer-Using-SDN
  ```
 2. ### Install Mininet and dependencies:
 ```
git clone https://github.com/mininet/mininet
mininet/util/install.sh -a
```
3. ### Install Python libraries system-wide:
```
sudo pip3 install ryu flask psutil requests werkzeug
```

## How to Start and Test the System
The system requires three separate terminal windows to run correctly.
### Terminal 1: Start the SDN Controller
```
cd /path/to/Load-Balancer-Using-SDN
ryu-manager load_balancer.py
```
You will see logs indicating the controller and web server have started.
### Terminal 2: Start the Mininet Network Topology
```
cd /path/to/Load-Balancer-Using-SDN
sudo python3 topology.py
```
This will create the virtual network and give you a mininet> command prompt.
### Terminal 3: Bridge the Host to the Mininet Network
The controller's monitor needs a network path to the Mininet hosts.
```
sudo ip addr add 10.0.0.254/24 dev sw1
sudo ip link set sw1 up
```
### Step 4: Start the Application Servers
Go back to Terminal 2 (mininet> prompt) and execute the following commands to start the smart web server on each virtual host.
```
mininet> s1 sudo python3 server_app.py &
mininet> s2 sudo python3 server_app.py &
mininet> s3 sudo python3 server_app.py &
```
ex: *s1 sudo python3 /home/mininet/msc-project/server_app.py &*

### Step 5: Access the Dashboard and Test
 1. Open a web browser on the machine running your VM.
 2. Navigate to http://<your_vm_ip>:8080/.
 3. The dashboard will load. Initially, servers may show as "DOWN". Within 5-10 seconds, the monitor will connect, and they will all turn green ("HEALTHY").
 4. Test normal load balancing: In the Mininet terminal, run h1 curl http://10.0.0.100:5000/ multiple times. Observe the changing "Hello from Server..." message.
 5. Test the adaptive feature: On the web dashboard, click the "Apply Load" button for any server. Watch the dashboard update in real-time as the server's status changes to "OVERLOADED" (yellow) and then recovers to "HEALTHY" (green). While it's overloaded, test with curl again to confirm traffic is being sent to the other healthy servers.
