import socket
import argparse
import threading
from queue import Queue
import pyfiglet
import time

parser = argparse.ArgumentParser()
parser.add_argument('host', metavar='Host', help='Target host url or ip address')
parser.add_argument('port_range', metavar='Port range', help='Port range (e.g 40-80)')
parser.add_argument('--timeout', metavar='Timeout', 
                    help='Socket timeout for scanning in seconds',
                    type=float, default=0.2)
parser.add_argument('-t', '--threads', metavar="Threads", help='Number of threads (default: 50)',
                     type=int, default=50)
args = parser.parse_args()

banner = pyfiglet.figlet_format("Port Scanner")
print(banner)

#target = input("Please enter host to scan: ")
target = args.host
try:
    target_ip = socket.gethostbyname(target)
except Exception as e:
    print("Invalid Host: ", e)
    exit()

print("Target: " + target)
print("Host: " + target_ip)

def get_port_range():
    try:
        port_list = args.port_range.split('-')
        start_port, end_port = map(int, port_list)
        if start_port >= 0 and end_port <= 65535 and start_port <= end_port:
            return start_port, end_port
        else:
            raise ValueError
    except:
        print("Invalid port range entered, the format is 0-65535 (start-end) port")
        exit()



port_queue = Queue()
start_port, end_port = get_port_range()
for port in range(start_port, end_port + 1):
    port_queue.put(port)

def scan_ports():
    while not port_queue.empty():
        port = port_queue.get()
        # AF_INET is for IPV4 addressing, SOCK_STREAM is TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(args.timeout)
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            try:
                service_banner = sock.recv(1024).decode().strip()
            except Exception:
                service_banner = "Banner Error"
            try: 
                expected_port = socket.getservbyport(port, 'tcp').upper() 
            except Exception:
                expected_port = "Unknown"
            print('Port {} Open | Expected Service: {} | {}'.format(port, expected_port, service_banner))
        sock.close()
        port_queue.task_done()

if __name__ == '__main__':
    start_time = time.time()
    threads = []

    for _ in range(args.threads):
        t = threading.Thread(target=scan_ports)
        t.daemon = True
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    time_taken = round((time.time() - start_time), 3)
    print("Ports {} to {} successfully scanned".format(start_port, end_port))
    print("Port Scanning took {}".format(time_taken))