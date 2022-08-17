import cv2
import pyautogui
import numpy as np
import os
import time


def callback(x):
    print(x)

#os.system("open -a 'Google Chrome' https://tiktok.com")
#time.sleep(15)
start_row = 110
end_row = 240
start_column = 0
end_column = 120

img = pyautogui.screenshot(region=(1100,622,670,425))
img = np.array(img)
print(img.shape)

img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
"""first try using 200,255, then use 150,255 if first try fails"""
#f, threshInv = cv2.threshold(img1, 150,255, cv2.THRESH_BINARY) #promising, keep this
f, threshInv = cv2.threshold(img1, 220,255, cv2.THRESH_BINARY_INV)

##METHODS
methods = [cv2.TM_CCOEFF]

pyautogui.moveTo(555,550,2)

cv2.createTrackbar('L', 'image', 0, 255, callback)
cv2.createTrackbar('U', 'image', 0, 255, callback)

while(1):
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    l = cv2.getTrackbarPos('L', 'image')
    u = cv2.getTrackbarPos('U', 'image')

    canny = cv2.Canny(threshInv, l, u)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(canny, contours, -1, (255,255,255), 3)
    template = canny[start_row:end_row, start_column:end_column]
    h1, w1 = template.shape

    for method in methods:
        newcan = canny.copy()
        newcan1 = newcan.copy()
        newcan1 = newcan[0:425, 125:670]
        result = cv2.matchTemplate(newcan1, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            location = min_loc
        else:
            location = max_loc
        print("old location: ",location)
        location = (location[0]+125, location[1])
        print("new location: ",location)
        bottom_right = (location[0] + w1, location[1] + h1)
        cv2.rectangle(newcan, location, bottom_right, 255, 5)
        #cv2.imshow('Match', )

    h, w = canny.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)


    numpy_horizontal_concat = np.concatenate((threshInv, canny, img1))
    cv2.imshow('THRESHOLD', newcan)
    time.sleep(2)
    break
pyautogui.click(button='left')
time.sleep(1)


pyautogui.dragTo(555 + location[0]/2, 550, 10, button="left")
cv2.destroyAllWindows()
