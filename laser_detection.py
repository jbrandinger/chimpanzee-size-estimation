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
    ret3, thresh = cv2.threshold(blur, 210, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Dilation to enlarge dots (tune parameters as needed)
    thresh = cv2.dilate(thresh, (5, 5), iterations=28)

    # Blob detection
    blobs = blob_log(thresh, max_sigma=50, threshold=0.15)
    count =0
    points = []
    if blobs.size != 0:  #checks if a blob was found
    # ax[1].imshow(thresh, cmap='gray')
        for blob in blobs[:2,:]:
            y, x, area = blob
            if area>1:   #checks for area of blob
                count +=1
                points.append((int(x),int(y)))
    
    else:
        print("No lasers detected")
    
    return points