from adafruit_rplidar import RPLidar
from math import floor
from threading import Thread

class LiDar:
    def __init__(self, port):
        self.lidar = RPLidar(None, port, timeout=3)
        self.data = [0]*360
        self._thread = Thread(target=self._event_loop)
        self._thread.start()
        self._stop = False
        self.ready = False
    
    def _event_loop(self):
        for scan in self.lidar.iter_scans():
            if self._stop: return
            data = [0]*360
            for (_, angle, distance) in scan:
                data[min([359, floor(angle)])] = distance
            self.data = data
            self.ready = True
    
    def stop(self):
        self._stop = True
        self.lidar.stop()
        self.lidar.disconnect()
