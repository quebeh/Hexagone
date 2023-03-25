from flask import Flask, Response, request
from hardware import Car, getPCA
import cv2 as cv
from numpy import concatenate

car = Car(getPCA(), 15, 0, 0)

app = Flask('Car')
indexhtml = open('client.html').read()
middle = 80
turnangle = 30
car.servo.turn(middle)

@app.route('/')
def index():
    return indexhtml

@app.route('/img')
def img():
    car.updateCamera()
    dsize = (car.camera.img.shape[1], car.camera.img.shape[0])
    img = car.camera.img if car.camera.matrix is None else concatenate([car.camera.img, cv.resize(car.camera.thresholdedImage, dsize)], axis=1)
    r = Response(cv.imencode('.png', img)[1].tobytes())
    r.headers['Content-Type'] = 'image/png'
    return r

@app.route('/setSpeed', methods=['POST'])
def setSpeed():
    car.speed = int(request.args['speed'])
    return 'ok'

@app.route('/turn', methods=['POST'])
def turn():
    car.servo.turn(80+(turnangle*int(request.args['steer'])))

app.run(port=8000)
