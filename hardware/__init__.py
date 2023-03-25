from .servo import Servo
from .esc import ESC
from .camera import CameraHandler
from threading import Thread

def getPCA(frequency=60):
    from adafruit_pca9685 import PCA9685
    from board import SCL, SDA
    from busio import I2C
    pca = PCA9685(I2C(SCL, SDA))
    pca.frequency = frequency
    return pca

class Car:
    def __init__(self, pca, escChannel: int, steerChannel: int, camera):
        self.pca = pca
        self.esc = ESC(self.pca.channels[escChannel])
        self.servo = Servo(self.pca.channels[steerChannel])
        self.camera = CameraHandler(camera)
        self.turn = self.servo.turn
        self._thread = None
    
    @property
    def speed(self):
        return self.esc.speed
    
    @speed.setter
    def speed(self, val):
        self.esc.speed = val
    
    @property
    def angle(self):
        return self.servo.angle
    
    @angle.setter
    def angle(self, val):
        self.servo.turn(val)
    
    def updateCamera(self):
        self.camera.update()

    @property
    def prediction(self):
        return self.camera.prediction

    def start(self):
        def event_loop():
            while True:
                self.camera.update()
        self._thread = Thread(target=event_loop)
        self._thread.start()
