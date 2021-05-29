import cv2
import numpy as np
from time import sleep

width_min=80 #Largura minima do retangulo
height_min=80 #Altura minima do retangulo

offset=6 # Permitted pixel-level error

pos_hline=285 # Y-Position of horizontal line

delay= 60 # FPS for video

detect = []
vehicles= 0

	
def page_center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('highway3.mp4')
#cap = cv2.VideoCapture('video.avi')

# Object Detection from Stable Camera
obj_detect = cv2.createBackgroundSubtractorMOG2()


while True:
    
    ret,frames = cap.read()

    tempo = float(1/delay)
    sleep(tempo)

    grey = cv2.cvtColor(frames,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)

    mask = obj_detect.apply(blur)

    ret, thresh = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    # apply image dilation
    kernel = np.ones((3,3),np.uint8)
    dilated = cv2.dilate(thresh,kernel,iterations = 1)

    # New Kernel and Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    dilation_n = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    dilation_n = cv2.morphologyEx(dilation_n, cv2.MORPH_CLOSE, kernel)

    # Countours
    #countours, h = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    countours, h = cv2.findContours(dilation_n, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frames, (0,pos_hline), (960,pos_hline), (100,0,255))
    #cv2.line(frames, (500,300), (800,300), (100,0,255))

    # find contours
    #contours, hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(dilation_n,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    for(index, c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        #print(f'w: {w}, h: {h}')
        valid_contour = (w >= width_min) and (h >= height_min)
        if not valid_contour:
            continue

        cv2.rectangle(frames, (x,y), (x+w, y+h), (0,255,0), 2)
        center = page_center(x,y,w,h)
        detect.append(center)
        cv2.circle(frames, center, 4, (0,0,255), -1)

        for(x,y) in detect:
            if y < (pos_hline + offset) and y > (pos_hline - offset):
                vehicles += 1
                detect.remove((x,y))
                #print("Vehicle detected: " + str(vehicles))

    cv2.putText(frames, "VEHICLE COUNT : "+str(vehicles), (10, 385), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    average = int(vehicles/37)
    
    if(average > 0):
        cv2.putText(frames, "Average : "+str(average), (400, 385), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Frames", frames)
    #cv2.imshow("Grey", grey)
    #cv2.imshow("Blur", blur)
    #cv2.imshow("Mask", mask)
    #cv2.imshow("Threshold", thresh)
    #cv2.imshow("Dilated", dilated)

    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
cap.release()
