import socket
import subprocess
import sys
from datetime import datetime
from .PortScanResponse import PortScanResponse


class PortScanner(object):

    def __init__(self):
        try:
            server_address = input('Host address: ')
            self.server_ip = socket.gethostbyname(server_address)
            self.min_port = int(input('lowest port: '))
            self.max_port = int(input('highest port: ')) + 1
            self.port_range = range(self.min_port, self.max_port)
        except socket.gaierror:
            print("Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print('Could not connect to server')
            sys.exit()

    def scan(self):
        subprocess.call('cls', shell=True)

        try:
            print('Scanning host: '.format(self.server_ip))
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
