import hardware

car = hardware.Car(hardware.getPCA(), 15, 0, 0)
car.speed = 1
middle = 110
turnangle = 30

while True:
    car.camera.update()
    if car.prediction != None:
        car.servo.turn(middle+(turnangle*car.prediction))
