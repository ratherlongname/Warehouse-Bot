import cv2
from qr import solve as qr_solve
from helpers import taninv
from motor import *
if __name__ == "__main__":
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
	cap.set(cv2.CAP_PROP_FPS, 30)
	while cap.isOpened():
		if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:
			cap.release()
			cv2.destroyAllWindows()
		ret, frame = cap.read()
		if not ret:
			cap.release()
			cv2.destroyAllWindows()
			raise Exception("Could not grab frame")
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		retval = qr_solve(gray)
		if retval is None:
			continue
		print(retval)
		rotation_offset = (taninv(retval[1][1] - retval[2][1], retval[1][0] - retval[2][0]) - 135) % 360
		if rotation_offset > 180:
			rotation_offset -= 360
		if rotation_offset > 20:
			drive('l', rotation_offset)
		elif rotation_offset < -20:
			drive('r', -rotation_offset)

	cap.release()
	cv2.destroyAllWindows()
