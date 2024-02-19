import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from skimage.feature import blob_log


def detect_laser_points(image, source):
    # Convert from BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define new HSV range for red laser points
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Apply Gaussian blur
    blurred_mask = cv2.GaussianBlur(red_mask, (15, 15), 0)

    # Apply threshold
    _, thresh = cv2.threshold(blurred_mask, 127, 255, cv2.THRESH_BINARY)

    # Dilate to make the laser points more visible
    dilated_thresh = cv2.dilate(thresh, None, iterations=2)

    # Detect blobs
    blobs = blob_log(dilated_thresh, max_sigma=30, num_sigma=10, threshold=0.1)

    # Process blobs
    points = []
    for blob in blobs:
        y, x, r = blob
        cv2.circle(source, (int(x), int(y)), int(r), (0, 255, 0), 2)
        points.append((int(x), int(y)))

    return source, points