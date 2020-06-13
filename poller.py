import time
import json
import requests


def now_ms():
    '''
    Return the current timestamp in milliseconds
    '''
    return int(round(time.time() * 1000))
    

class SensorPoller:
    def __init__(self, ip_port='localhost:8888'):
        self._initial_ts = now_ms()-10000
        self._prev_max_ts = -1
        self._url = 'http://{ip_port}/sensors.json'.format(ip_port=ip_port)
    
    def __read_url(self, min_ts):
        '''
        perform a get request from the url; 
        and return those that has (timestamp-initial_ts) > min_ts 
        '''
        r = requests.get(self._url, verify=False)
        sensors_json = json.loads(r.content)
        data = sensors_json['gravity']['data']
        gravities = [(row[0]-self._initial_ts, *row[1]) for row in data if (row[0]-self._initial_ts > min_ts)] 
        return gravities # list of tuples (ts, x, y, z)
        
    def get_next(self):
        curr = self.__read_url(self._prev_max_ts) 
        self._prev_max_ts = curr[-1][0]
        return curr
