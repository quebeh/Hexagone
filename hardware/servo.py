from adafruit_pca9685 import PWMChannel

class Servo:
    def __init__(self, channel: PWMChannel, min_pulse: int = 750, max_pulse: int = 2250):
        self.pca = channel
        self.min_duty = int((min_pulse * channel.frequency) / 1000000 * 0xffff)
        self.duty_range = int(((max_pulse * channel.frequency) / 1000000 * 0xFFFF)-self.min_duty)
        self.angle = 0
        
    def turn(self, angle: float):
        self.angle = angle
        self.pca.duty_cycle = self.min_duty + int((angle/180) * self.duty_range)
