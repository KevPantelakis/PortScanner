from PortScanner import PortScanner
from PortScanner import ThreadedPortScanner
import argparse


def t_scan():
    scanner = ThreadedPortScanner()
    scanner.scan()


def s_scan():
    scanner = PortScanner()
    scanner.scan()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help='Uses a single thread to accomplish the scan', action='store_true')
    parser.add_argument('-t', help='Uses several threads to accomplish the scan', action='store_true')
    args = parser.parse_args()
    if args.s:
        s_scan()
    else:
        t_scan()

