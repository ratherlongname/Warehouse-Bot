import numpy as np
import cv2
from cv2 import aruco

def solve(gray):
    if len(gray.shape) == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50) # pylint: disable=no-member
    parameters = aruco.DetectorParameters_create() # pylint: disable=no-member
    corners, ids, rejectedImgPoints = aruco.detectMarkers( # pylint: disable=no-member
        gray, aruco_dict, parameters=parameters)
    print(corners, ids, rejectedImgPoints)
    gray = aruco.drawDetectedMarkers(gray, corners) # pylint: disable=no-member


def save(uid, size=50):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50) # pylint: disable=no-member
    img = aruco.drawMarker(aruco_dict, uid, size)  # pylint: disable=no-member
    k = np.full((100, 100), 255, np.uint8)
    k[25:75, 25:75] = img
    # ch3 = np.empty((size, size, 3), dtype=np.uint8)
    # ch3[:, :, 0] = img
    # ch3[:, :, 1] = img
    # ch3[:, :, 2] = 255
    # solve(img)
    cv2.circle(k, (0,0), 5, 0, -1)
    cv2.imwrite(f"{uid}.jpg", k)
    # cv2.imshow('aruco', k)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

for i in range(50):
    save(i, 50)
# save(0,50)
