import socket
import subprocess
import sys
from datetime import datetime
import time
import random
import math
import concurrent.futures


class PortScanResponse:
    def __init__(self, port_number, status):
        self.port_number = port_number
        self.port_status = status

    def pretty_print(self):
        if self.port_status:
            print("Port {}:         Open".format(self.port_number))
        else:
            print("Port {}:       Closed".format(self.port_number))


class ThreadedPortScanner(object):

    def __init__(self):
        server_address = 'www.google.com'  # input('Host address: ')
        self.server_ip = socket.gethostbyname(server_address)
        self.min_port = int(input('lowest port: '))
        self.max_port = int(input('highest port: ')) + 1
        self.port_range = range(self.min_port, self.max_port)

    def scan(self):
        subprocess.call('cls', shell=True)

        try:

            print('Scanning host: ', self.server_ip)

            # Split range equally
            max_workers = math.ceil((len(self.port_range))/5)
            start = datetime.now()

            # start threads for each split range
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                if max_workers > 1:
                    low = self.min_port
                    high = self.min_port + 5
                    print("Will use {} threads".format(max_workers))
                    futures = list()
                    for i in range(0, max_workers):
                        rng = range(low, high)
                        print('starting thread #{} for ports {} to {}'.format(i + 1, low, high - 1))
                        # futures.append(executor.submit(self.fake_scan, rng))
                        futures.append(executor.submit(self.start_scan, rng))
                        low = low + 5
                        high = min(high + 5, self.max_port)

                    scan_responses = list()
                    for future in futures:
                        scan_responses.append(future.result())

                    for responses in scan_responses:
                        for response in responses:
                            response.pretty_print()
                else:
                    rng = range(self.min_port, self.max_port)
                    print("starting thread #{} for ports {} to {}".format(1, self.min_port, self.max_port - 1))
                    # future = executor.submit(self.fake_scan, rng)
                    future = executor.submit(self.start_scan, rng)
                    for result in future.result():
                        result.pretty_print()

        except KeyboardInterrupt:
            print("Ctrl+C was detected stopping scan now")
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print('Could not connect to server')
            sys.exit()

        print('Scan completed in {}'.format(datetime.now() - start))

    def fake_scan(self, port_range):
        lst = list()
        for port in port_range:
            result = random.randint(0, 1)
            lst.append(PortScanResponse(port, result))
            time.sleep(0.3)
        return lst

    def start_scan(self, port_range):
        lst = list()
        for port in port_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.server_ip, port))
            lst.append(PortScanResponse(port, result))
            sock.close()
        return lst


class PortScanner(object):

    def __init__(self):
        server_address = 'www.google.com'  # input('Host address: ')
        self.server_ip = socket.gethostbyname(server_address)
        self.min_port = int(input('lowest port: '))
        self.max_port = int(input('highest port: ')) + 1
        self.port_range = range(self.min_port, self.max_port)

    def scan(self):
        subprocess.call('cls', shell=True)

        try:
            print('Scanning host: ', self.server_ip)
            start = datetime.now()
            results = self.start_scan(self.port_range)
            # start threads for each split range
            for result in results:
                result.pretty_print()

        except KeyboardInterrupt:
            print("Ctrl+C was detected stopping scan now")
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print('Could not connect to server')
            sys.exit()

        print('Scan completed in {}'.format(datetime.now() - start))

    def start_scan(self, port_range):
        lst = list()
        for port in port_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.server_ip, port))
            lst.append(PortScanResponse(port, result))
            sock.close()
        return lst
