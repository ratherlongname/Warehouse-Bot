import qrcode
from secrets import randbelow as r
import sys, uuid
import cv2, os
import numpy as np

def make_qr(data, angle):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=False)
    img = qr.make_image(fill_color="black", back_color="white")
    # img.save(f"test_images/qr_{data}.png")
    img = np.array(img, dtype="uint8")*255
    h, w = img.shape[:2]
    img = cv2.bitwise_not(img)
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, r(100)*0.004+0.6)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    img = cv2.warpAffine(img, M, (nW, nH))
    img = cv2.bitwise_not(img)
    _, img, _, _ = cv2.floodFill(img, None, (0, 0), 255)
    h, w = img.shape
    res = np.full((1000, 1000), 255, dtype="uint8")
    x, y = r(1000 - h), r(1000 - w)
    res[x: x + h, y: y + w] = img
    name = f'test_images/qr_{format(angle, "03d")}_{format(x, "03d")}_{format(y, "03d")}_{format(h, "03d")}_{data}.png'
    print(name)
    cv2.imwrite(name, res)

if len(sys.argv) == 2:
    data = sys.argv[1]
    angle = r(360)
    make_qr(data, angle)
elif len(sys.argv) == 3:
    data = sys.argv[1]
    angle = int(sys.argv[2])
    if angle == 0:
        angle = r(360)
    make_qr(data, angle)
else:
    for i in range(15):
        data = uuid.uuid4().hex[:7]
        angle = r(360)
        make_qr(data, angle)
