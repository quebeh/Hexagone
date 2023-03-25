from adafruit_pca9685 import PWMChannel

class ESC:
    CALIBRATION_DUTY = 5000
    FORWARD_MIN = 7000
    FORWARD_MAX = 8000
    BACKWARD_MIN = 3500
    BACKWARD_MAX = 4000

    def __init__(self, channel: PWMChannel):
        self.controller = channel
        self._speed = 0

        for i in range(self.CALIBRATION_DUTY):
            self.controller.duty_cycle = i
            print(f'\rCalibrating ESC on channel {channel}... {round((i/self.CALIBRATION_DUTY)*100)}%', end='')
        print('\nDone calibrating')
        self.controller.duty_cycle = 0

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, val):
        if not -1 <= val <= 1:
            raise ValueError("Speed must be between -1 and 1")
        if val == 0:
            self.controller.duty_cycle = 0
        elif val > 0:
            self.controller.duty_cycle = int(self.FORWARD_MIN + ((self.FORWARD_MAX-self.FORWARD_MIN)*val))
        elif val < 0:
            self.controller.duty_cycle = int(self.BACKWARD_MIN + ((self.BACKWARD_MAX-self.BACKWARD_MIN)*abs(val)))
