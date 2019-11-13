import cv2
from cv2 import aruco
import pyzbar.pyzbar as pyzbar
import config
def marker_solve(gray):
    '''
    solves qr or aruco code depending on config var
    returns : `data, top, center` or `None`
    '''
    if config.USE_QR:
        return qr_solve(gray)
    return aruco_solve(gray)

def setup_webcam():
    ''' returns cap object '''
    cap = cv2.VideoCapture(0)#, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
    cap.set(cv2.CAP_PROP_FPS, 30)
    if not cap.isOpened():
        raise Exception("Camera not working")
    return cap


def get_frame(cap):
    ''' returns a frame from cap '''
    ret, frame = cap.read()
    if not ret:
        raise Exception("Camera read failed")
    return frame


def qr_solve(gray):
    '''
    solves qr code
    returns : `data, top, center` or `None`
    '''
    if len(gray.shape) == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    qrcode = pyzbar.decode(gray, [pyzbar.ZBarSymbol.QRCODE])
    if len(qrcode) != 1:
        return None
    qrcode = qrcode[0]
    x, y = 0, 0
    for i in qrcode.polygon:
        x += i[0]
        y += i[1]
    x = x // 4
    y = y // 4
    top = qrcode.polygon[0]
    return qrcode.data, top, (x, y)


def aruco_solve(gray):
    '''
    solves aruco code
    returns : `data, top, center` or `None`
    '''
    if len(gray.shape) == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)  # pylint: disable=no-member
    parameters = aruco.DetectorParameters_create()  # pylint: disable=no-member
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)  # pylint: disable=no-member
#    if corners is not None and len(corners) !=0:
#        print(corners)
    # print(corners, ids, rejectedImgPoints)
    if ids is not None and len(ids[0]) == 1:
        corners = corners[0][0]
        ids = ids[0][0]
        #print(ids, corners)

        x, y = 0, 0
        for i in corners:
            x += i[0]
            y += i[1]
        x = int(x // 4)
        y = int(y // 4)
        return ids, (int(corners[0][0]), int(corners[0][1])), (x, y)
    return None


if __name__ == "__main__":
    raise Exception("This is not a top level module")
