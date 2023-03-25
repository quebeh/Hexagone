import cv2 as cv
import numpy as np
from typing import Tuple
from math import sqrt

def distance(p1, p2):
    return sqrt(((p2[0]-p1[0])**2)+((p2[1]-p1[1])**2))

class CameraHandler:
    class CameraEmptyError(Exception):
        pass

    class CameraUncalibratedError(Exception):
        pass

    LEFT = -1
    RIGHT = 1
    FORWARD = 0

    def __init__(self, camera, calibratePatternSize: Tuple[int] = (5,5), lowThreshold=65, highThreshold=255, capProp=None):
        self.cam = cv.VideoCapture(camera, capProp)
        self.matrix = None
        self.wnw, self.wnh = None, None
        self.lowThreshold = lowThreshold
        self.highThreshold = highThreshold
        self.warpedImage = None
        self.thresholdedImage = None
        self.prediction = None
        self.cps = calibratePatternSize
        self.cords = None
    
    def update(self):
        ret, self.img = self.cam.read()
        if not ret:
            raise CameraHandler.CameraEmptyError()
        try:
            self.warpedImage = self._warpedImage()
            self.thresholdedImage = self._thresholdedImage()
            self.houghLines = self._houghLines()
            self.prediction = self._predict()
        except CameraHandler.CameraUncalibratedError:
            self.calibrateCheckerboard()
        return True

    def _warpedImage(self):
        if self.matrix is None:
            raise CameraHandler.CameraUncalibratedError("Camera not calibrated. Use CameraHandler.calibrateCheckerboard()")
        return cv.warpPerspective(self.img, self.matrix, (self.wnw, self.wnh))
    
    def _thresholdedImage(self):
        return cv.cvtColor(
            cv.threshold(
                cv.cvtColor(self.warpedImage, cv.COLOR_BGR2GRAY),
                self.lowThreshold,self.highThreshold,cv.THRESH_TOZERO
            )[1], cv.COLOR_GRAY2BGR)
    
    def _houghLines(self):
        linepre = cv.GaussianBlur(cv.Canny(self.thresholdedImage, 0, 255), (5,5), 0)
        return cv.HoughLines(linepre, 1, np.pi / 180, 150, None, 0, 0)

    def _predict(self):
        if self.houghLines is not None:
            t = max([i[0][1] for i in self.houghLines])
            if 2.4 < t < 3.2:
                return CameraHandler.LEFT
            if 0 < t < 0.2 or 3.2 < t:
                return CameraHandler.FORWARD
            if 0.2 < t < 1:
                return CameraHandler.RIGHT

    def showThresholded(self):
        cv.imshow('Thresholded Image', self.thresholdedImage)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def calibrateCheckerboard(self):
        ret, im = self.cam.read()
        if not ret:
            return False
        gray = cv.threshold(cv.cvtColor(im, cv.COLOR_BGR2GRAY),self.lowThreshold,self.highThreshold,cv.THRESH_TOZERO)[1]
        ret, corners = cv.findChessboardCorners(gray, self.cps, None)
        if not ret:
            return False
        else:
            cords = self._checkerboardCornerCorners(corners)
            print([(i[0][0], i[0][1]) for i in corners])
            print('---')
            print([(i[0], i[1]) for i in cords])
            nw = max([distance(cords[i], cords[i-1]) for i in range(len(cords))])
            nh = nw*(im.shape[0]/im.shape[1])
            self.wnw = int(nw)
            self.wnh = int(nh)
            wharr = [[0, 0], [int(nw), 0], [0, int(nh)], [int(nw), int(nh)]]
            fc, fw = np.float32(cords), np.float32(wharr)
            self.cords = fc
            self.matrix = cv.getPerspectiveTransform(fc, fw)
            return True

    def _checkerboardCornerCorners(self, cords):
        x = self.cps[0]
        y = self.cps[1]
        return [cords[0][0], cords[x-1][0], cords[x*(y-1)][0], cords[(x*y)-1][0]]

    # @staticmethod
    # def _checkerboardCornerCorners(corners):
    #     maxy = None
    #     miny = None
    #     maxyc = None
    #     minyc = None
    #     maxx = None
    #     minx = None
    #     maxxc = None
    #     minxc = None
    #     for j in corners:
    #         i = int(j[0][0]), int(j[0][1])
    #         if maxy is None:
    #             maxy = i[1]
    #             miny = i[1]
    #             maxyc = [i]
    #             minyc = [i]
    #             maxx = i[1]
    #             minx = i[1]
    #             maxxc = [i]
    #             minxc = [i]
            
    #         if i[1] == maxy:
    #             maxyc.append(i)
    #         elif i[1] > maxy:
    #             maxy = i[1]
    #             maxyc = [i]
    #         if i[1] == miny:
    #             minyc.append(i)
    #         elif i[1] < miny:
    #             miny = i[1]
    #             minyc = [i]
            
    #         if i[0] == maxx:
    #             maxxc.append(i)
    #         elif i[0] > maxx:
    #             maxx = i[0]
    #             maxxc = [i]
    #         if i[0] == minx:
    #             minxc.append(i)
    #         elif i[0] < minx:
    #             minx = i[0]
    #             minxc = [i]
        
    #     if len(minyc) == 1 and len(maxyc) == 1 and len(maxxc) == 1 and len(minxc) == 1:
    #         if minxc[0][1]>maxxc[0][1]:
    #             ii = minyc[0]
    #             ai = maxxc[0]
    #             ia = minxc[0]
    #             aa = maxyc[0]
    #         else:
    #             ii = minxc[0]
    #             ai = minyc[0]
    #             ia = maxyc[0]
    #             aa = maxxc[0]
    #     elif len(minyc) > 1 and len(maxyc) > 1:
    #         ii = min(minyc, key=lambda x:x[0])
    #         ai = max(minyc, key=lambda x:x[0])
    #         ia = min(maxyc, key=lambda x:x[0])
    #         aa = max(maxyc, key=lambda x:x[0])
    #     elif len(minxc) > 1 and len(maxxc) > 1:
    #         ii = min(minxc, key=lambda x:x[1])
    #         ai = min(maxxc, key=lambda x:x[1])
    #         ia = max(minxc, key=lambda x:x[1])
    #         aa = max(maxxc, key=lambda x:x[1])
    #     else:
    #         ii = minxc[0]
    #         ai = minyc[0]
    #         ia = maxyc[0]
    #         aa = maxxc[0]
        
    #     return [
    #         tuple(ii), 
    #         tuple(ai), 
    #         tuple(ia), 
    #         tuple(aa)
    #     ]
