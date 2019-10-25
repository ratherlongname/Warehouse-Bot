import cv2, math, sys
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
import matplotlib.pyplot as plt
cv2.namedWindow('', cv2.WINDOW_NORMAL)
def show(data):
    cv2.imshow('', data)
    cv2.waitKey(1)

def euclidean_distance(p1, p2):
    #! WARNING: Returns square of actual euclidean distance
    return ((p1[1] - p2[1]) ** 2 + (p1[0] - p2[0]) ** 2)

def find_moments(c):
    mu = cv2.moments(c, False)
    return ((mu['m10'] / (mu['m00'] + 1e-5)), (mu['m01'] / (mu['m00'] + 1e-5)))

def find_top(contours, heirarchy):
    # heirarchy ~~ [Next, Previous, First_Child, Parent]
    markers = [] # Stores TL, TR, BL markers
    for i in range(len(contours)):
        k = i
        c = 0
        while heirarchy[k][2] != -1:
            k = heirarchy[k][2]
            c += 1
        if heirarchy[k][2] != -1:
            c += 1
        if c >= 2:
            markers.append(i)
    markers = list(set(markers))
    if len(markers) <3:
        return None
    m1 = find_moments(contours[markers[0]])
    m2 = find_moments(contours[markers[1]])
    m3 = find_moments(contours[markers[2]])
    # print(m1, m2, m3)
    ab = euclidean_distance(m1, m2)
    bc = euclidean_distance(m2, m3)
    ca = euclidean_distance(m3, m1)
    m = max((ab, m3), (bc, m1), (ca, m2))
    # print(m)
    return m[1]
def solve(original_gray):
    # original_gray = data
    #original_gray = cv2.resize(original_gray, dsize=None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR_EXACT)
    # show(original_gray, True, f'{desc} Original Gray', 'gray')
    inverted_gray = cv2.bitwise_not(original_gray)
    #data, bbox, _ = qr.detectAndDecode(original_gray)
    qrcodes = pyzbar.decode(original_gray)
    # assert len(qrcodes)==1
    if len(qrcodes) <1:
        return original_gray
    print(qrcodes[0].data)
    x,y,h,w = qrcodes[0].rect
    #bbox=[]
    #bbox = [(x,y),(x+h,y),(x+h,y+w),(x,y+w)]
    #assert bbox is not None
    #x, y, h, w = cv2.boundingRect(bbox)
    _, contours, heirarchy= cv2.findContours(inverted_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for cs in contours:
    #     q,w,e,r = cv2.boundingRect(cs)
    #     cv2.rectangle(original_gray, (q,w), (q+e,w+r), 127, 2)
    heirarchy = heirarchy[0]
    top = find_top(contours, heirarchy)
    if top is None:
        return original_gray
    #cx, cy = 0, 0
    #for pts in bbox:
    #    cx, cy = cx+pts[0][0], cy+pts[0][1]
    #    center = (cx/4, cy/4)
    center = (x + h/2, y+ w/2)
    # pp(top, i='top')
    # pp(center, i='centre')
    cv2.circle(original_gray, (int(top[0]), int(top[1])), 10, (255,0,0), -1)
    cv2.circle(original_gray, (int(center[0]), int(center[1])), 10, (255,0,0), -1)
    # show(disp, False, desc + " Features Extracted", None)

    dy = top[1] - center[1]
    dx = top[0] - center[0]
    slope = dy / dx
    deg  = math.degrees(math.atan(slope))
    print(slope, dy, dx, deg)
    return original_gray

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        show(solve(frame))

