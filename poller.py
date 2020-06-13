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
        gravity = sensors_json['gravity']['data']
        proximity = sensors_json['proximity']['data']
        rotation = sensors_json['rot_vector']['data']
        gyro = sensors_json['gyro']['data']
        lin_accel = sensors_json['lin_accel']['data']
        accel = sensors_json['accel']['data']
        magnetic = sensors_json['mag']['data']
        data = {
            'timestamp': [row[0]-self._initial_ts for row in gravity if (row[0]-self._initial_ts > min_ts)],
            'gravity': [(*row[1],) for row in gravity if (row[0]-self._initial_ts > min_ts)] ,
            'proximity': [(*row[1],) for row in proximity if (row[0]-self._initial_ts > min_ts)] ,
            'rotation': [(*row[1],) for row in rotation if (row[0]-self._initial_ts > min_ts)] ,
            'gyro': [(*row[1],) for row in gyro if (row[0]-self._initial_ts > min_ts)] ,
            'lin_accel': [(*row[1],) for row in lin_accel if (row[0]-self._initial_ts > min_ts)] ,
            'accel': [(*row[1],) for row in accel if (row[0]-self._initial_ts > min_ts)] ,
            'magnetic': [(*row[1],) for row in magnetic if (row[0]-self._initial_ts > min_ts)] ,
            }
        return data 
        
    def get_next(self):
        curr = self.__read_url(self._prev_max_ts) 
        self._prev_max_ts = curr['timestamp'][-1]
        return curr
