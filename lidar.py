from math import floor, cos, sin, radians
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from threading import Thread

PORT_NAME = 'COM9'
lidar = RPLidar(None, PORT_NAME, timeout=3)
x, y = [0]*360, [0]*360
fig, ax = plt.subplots()
sc = ax.scatter(x, y)

def scan():
    for scan in lidar.iter_scans():
        data = [0]*360
        for (_, angle, distance) in scan:
            data[min([359, floor(angle)])] = distance
        ax.clear()
        x = [cos(radians(i))*data[i] for i in range(len(data))]
        y = [sin(radians(i))*data[i] for i in range(len(data))]
        ax.scatter(x, y)
        minx = min(x)
        maxx = max(x)
        miny = min(y)
        maxy = max(y)
        xo = maxx - minx * 0.2
        yo = maxy - miny * 0.2
        mao = max(maxx+xo, maxy+yo)
        mio = min(miny-yo, maxy+yo)
        ax.add_artist(Circle((0, 0), max(mao, mio)*0.025, fc='red'))
        ax.set_xlim(mio, mao)
        ax.set_ylim(mio, mao)
        fig.canvas.draw()

scanner = Thread(target=scan)
scanner.start()

plt.show()

lidar.stop()
lidar.disconnect()
