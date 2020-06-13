#!/usr/bin/env python3
import signal
import sys
import time
from poller import SensorPoller

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # TODO write to file
    sys.exit(0)


def main():

    # register control c handler
    signal.signal(signal.SIGINT, signal_handler)

    poller = SensorPoller(ip_port='192.168.20.141:8888')
    while True:
        gravities = poller.get_next()
        print(len(gravities), gravities[0])
        time.sleep(0.2)


if __name__=='__main__':
    main()