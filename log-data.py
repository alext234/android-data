#!/usr/bin/env python3
import signal
import sys
import time
from poller import SensorPoller
import argparse
import pandas as pd

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # TODO write to file
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output','-o', required=True)
    parser.add_argument('--duration','-d', type=float, required=True)
    options = parser.parse_args()

    # register control c handler
    signal.signal(signal.SIGINT, signal_handler)

    poller = SensorPoller(ip_port='192.168.20.141:8888')
    period = 0.200

    l =[]
    print('start pulling data...')
    for i in range(int(options.duration/period)):
        l.append(poller.get_next())
        time.sleep(period)

    print('writing to file...')
    df = pd.DataFrame(l[0])
    for ldf in l[1:]:
        df = df.append(pd.DataFrame(ldf))
    df.to_csv(options.output, index=False)

if __name__=='__main__':
    main()