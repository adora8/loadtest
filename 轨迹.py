import numpy as np
import cv2

cap = cv2.VideoCapture('D:/360Downloads/wpcache/test.mp4')
feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7)
lk_params = dict(winSize=(15, 15),
                 maxLevel=2)
color = np.random.randint(0, 255, (0, 3))
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
mask = np.zeros_like(old_frame)
while(True):
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a, b), (c, d), (0,255,0), 2)
        frame = cv2.circle(frame, (a, b), 5, (255,0,0), -1)
        img = cv2.add(frame, mask)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(150) & 0xff
    if k == 27:
        break

    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cv2.destroyAllWindows()
cap.release()