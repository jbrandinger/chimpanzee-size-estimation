#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 20 2024

@author: jbrandinger

NAME: laser_detection.py

PURPOSE: 
    - detect red laser points on image

HOW TO USE:
    - provide 'detect_laser_points' with image containing red lasers

NOTES:
    - coordinates of laser points are returned as a list of tuples
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import blob_log


def detect_laser_points(img):
    # Assuming 'img' is your input image
    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert from BGR to HSV

    # Define two ranges for red (due to the circular nature of the hue scale in HSV)
    low_red1 = np.array([0, 120, 70])
    high_red1 = np.array([10, 255, 255])
    low_red2 = np.array([170, 120, 70])
    high_red2 = np.array([180, 255, 255])

    # Create masks for the red ranges
    red_mask1 = cv2.inRange(hsv_frame, low_red1, high_red1)
    red_mask2 = cv2.inRange(hsv_frame, low_red2, high_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Apply mask to the image
    red = cv2.bitwise_and(img, img, mask=red_mask)

    # Extract red channel for processing (assuming red dots are the brightest in the red channel)
    r = red[:,:,2]

    # Apply Gaussian blur for smoothing
    blur = cv2.GaussianBlur(r, (25, 25), 0)

    # Apply thresholding
    _, thresh = cv2.threshold(blur, 210, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Dilation to enlarge dots (tune parameters as needed)
    # thresh = cv2.dilate(thresh, (5, 5), iterations=28) # maybe change ?
    thresh = cv2.dilate(thresh, None, iterations=2)


    # Blob detection
    # blobs = blob_log(thresh, max_sigma=50, threshold=0.15)
    blobs = blob_log(thresh, max_sigma=30, num_sigma=10, threshold=.1)
    blobs = sorted(blobs, key=lambda b: b[1])

    min_distance_px = 40 # minimum number of pixels apart
    points = []
    for blob in blobs:
        y, x, r = blob
        if r > 1:  # Check for area of blob
            # Check if this blob is far enough from the last one
            if not points or (x - points[-1][0])**2 + (y - points[-1][1])**2 >= min_distance_px**2:
                points.append((int(x), int(y)))

    if len(points) < 2:
        print("Less than two lasers detected")

    return points[:2]  # Return only the first two points