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
        rotation = sensors_json['rot_vector']['data']
        gyro = sensors_json['gyro']['data']
        lin_accel = sensors_json['lin_accel']['data']
        accel = sensors_json['accel']['data']
        magnetic = sensors_json['mag']['data']
        
        ts_list = [row[0]-self._initial_ts for row in gravity if (row[0]-self._initial_ts > min_ts)]
        max_ts = ts_list[-1]
        for t in [ rotation, gyro, lin_accel, accel, magnetic ]:
            ts_list1 = [row[0]-self._initial_ts for row in t if (row[0]-self._initial_ts > min_ts)]
            if ts_list1[-1]<max_ts: # the min of all the max
                max_ts = ts_list1[-1]
            if len(ts_list1) < len(ts_list): # use the shorter list of timestamp
                ts_list = ts_list1

        ts_len = len(ts_list)

        data = {
            'timestamp': ts_list,
            'gravity': [(*row[1],) for row in gravity if (row[0]-self._initial_ts > min_ts)][:ts_len] ,
            'rotation': [(*row[1],) for row in rotation if (row[0]-self._initial_ts > min_ts)][:ts_len] ,
            'gyro': [(*row[1],) for row in gyro if (row[0]-self._initial_ts > min_ts)][:ts_len] ,
            'lin_accel': [(*row[1],) for row in lin_accel if (row[0]-self._initial_ts > min_ts)][:ts_len] ,
            'accel': [(*row[1],) for row in accel if (row[0]-self._initial_ts > min_ts)][:ts_len] ,
            'magnetic': [(*row[1],) for row in magnetic if (row[0]-self._initial_ts > min_ts)][:ts_len] ,
            }
        return data, max_ts
        
    def get_next(self):
        curr, max_ts = self.__read_url(self._prev_max_ts) 
        self._prev_max_ts = max_ts
        return curr

