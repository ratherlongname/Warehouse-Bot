from helpers import *
from qr import *
import cv2
import numpy as np

if __name__ == "__main__":
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
	cap.set(cv2.CAP_PROP_FPS, 30)
	cv2.namedWindow("qr", cv2.WINDOW_NORMAL)
	cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			cap.release()
			cv2.destroyAllWindows()
			raise Exception("Could not grab frame")
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		retval = solve(gray)
		if retval is not None:
			print(retval[0])
			top = retval[1]
			center = retval[2]
			print(taninv(top[1]-center[1], top[0]-center[0]))
			cv2.circle(frame, top, 5, (255, 0, 0), -1)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			cv2.imshow("qr", frame)
		cv2.imshow("frame", frame)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cap.release()
	cv2.destroyAllWindows()
