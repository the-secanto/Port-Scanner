A simple multithreaded TCP port scanner built in Python.
The goal of this project was not to recreate Nmap, but to understand how it works.

**Features**
Multithreaded TCP port scanning
Customizable thread count
Socket timeout setting
Basic banner grabbing
Service detection using known port mappings

**How It Works**
Resolves the target hostname to an IP address.
Generates a queue of ports based on the provided range.
Uses multiple threads to:
Attempt TCP connections
Identify open ports
Attempt to retrieve service banners
Detect expected services using socket.getservbyport
Outputs open ports along with expected services.

Example Usage
python scanner.py localhost 0-450 -t 200

This command:
Scans localhost
Checks ports 0–450
Uses 200 threads to increase scanning speed

Example Output
Port 22 Open | Expected Service: SSH | OpenSSH 8.2p1
Port 80 Open | Expected Service: HTTP | Apache/2.4.49
Ports 0 to 450 successfully scanned
Port Scanning took 0.842 seconds

**What I Learned:**

This project helped me understand:
How the TCP handshake works
How a tool like Nmap is programmed/created
Why Nmap uses advanced techniques like SYN scans instead of full TCP connections

This project strengthened my understanding of:
Networking fundamentals (TCP/IP)
Socket programming in Python
Multithreading with threading and Queue

**Note: This tool was designed for educational purposes and should never be used to harm another person. Port scanning/Nmap scans on websites/networks you do not personally own can be considered intrusive and in many cases illegal.**
