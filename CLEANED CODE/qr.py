import math

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

def solve(original_gray):
	qrcode = pyzbar.decode(original_gray, [pyzbar.ZBarSymbol.QRCODE])
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
			cv2.circle(frame, retval[1], 5, (255, 0, 0), -1)
			cv2.circle(frame, retval[2], 5, (0, 0, 255), -1)
			cv2.imshow("qr", frame)
		cv2.imshow("frame", frame)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cap.release()
	cv2.destroyAllWindows()
