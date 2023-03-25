from hardware.camera import CameraHandler
import cv2 as cv
from numpy import concatenate

camera = CameraHandler(0, lowThreshold=100, highThreshold=150, capProp=cv.CAP_DSHOW)
d = False

while True:
    if d:
        d = not camera.calibrateCheckerboard()
    camera.update() 
    im = camera.img
    if camera.cords is not None:
        for i in camera.cords:
            cv.circle(im, (int(i[0]), int(i[1])), 5, (0, 0, 255))
    cv.imshow('Camera', im)
    try:
        half = (int(camera.img.shape[0]/2), int(camera.img.shape[1]/2))
        p = 'Right' if camera.prediction == 1 else ('Left' if camera.prediction == -1 else 'Forward')
        cv.imshow(
            'Result',
            cv.putText(
                concatenate((cv.resize(camera.warpedImage, half), cv.resize(camera.thresholdedImage, half)), axis=1), 
                f'Prediction: {p}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
        )
    except:
        pass

    k = cv.waitKey(33)
    if k == 27:
        cv.destroyAllWindows()
        break
    elif k == ord('d') & 0xFF:
        d = True
