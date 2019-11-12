import cv2
from helpers import taninv
# import numpy as np
from marker import marker_solve

METHOD = 'aruco'  # or 'qr'

if __name__ == "__main__":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
    cap.set(cv2.CAP_PROP_FPS, 30)
    # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.namedWindow("qr", cv2.WINDOW_NORMAL)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

    while cap.isOpened():
        ret, frame = cap.read()
        # frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # mask = cv2.inRange(frame_hsv, (0, 50, 20), (5, 255, 255))
        # mask2 = cv2.inRange(frame_hsv, (175, 50, 20), (180, 255, 255))
        # mask = cv2.bitwise_or(mask, mask2)
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            raise Exception("Could not grab frame")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        retval = marker_solve(gray)
        if retval is not None:
            top = retval[1]
            center = retval[2]
            print(taninv(top[1]-center[1], top[0]-center[0]))
            cv2.circle(frame, top, 5, (255, 0, 0), -1)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.imshow("qr", frame)
        cv2.imshow("frame", gray)
        # cv2.imshow("mask", mask)
        keypress = cv2.waitKey(1)
        if keypress & 0xff == ord("s"):
            cv2.imwrite("a.png", frame)
        elif keypress & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
