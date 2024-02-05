import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from skimage.feature import blob_log


def detect_laser_points(mask, source):   
    hsv_frame = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV) #convert from BGR to HSV 

    low_green = np.array([55, 110, 110])  #low_green values for green mask
    high_green = np.array([65, 255, 255]) #high_green values for green mask
    green_mask = cv2.inRange(hsv_frame, low_green, high_green) #performs basic threshold
    green = cv2.bitwise_and(mask, mask, mask=green_mask)#performs bitwise and operation

    g = green[:,:,1] #extracts the green channel
    blur = cv2.GaussianBlur(g,(25,25),0) #adds blurring for smoothing
    _,thresh = cv2.threshold(blur,210,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    
    thresh = cv2.dilate(thresh,(5,5),iterations=28) #adds dilation to enlarge dots a bit can be tuned with the arguments

    blobs = blob_log(thresh, max_sigma=50, threshold=0.15) # blob detection
    if blobs.size != 0:  #checks if a blob was found
        points = []
        for blob in blobs[:2,:]:
            y, x, area = blob
            if area>1:   #checks for area of blob
                points.append((int(x),int(y)))
                result1 = cv2.circle(source, (int(x),int(y)),12,(0,0,255),-1) # draws circles on detected blob

    return result1, points