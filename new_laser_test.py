import cv2
import numpy as np


def find_lasers(image):
    # Step 2: Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Step 3: Define the range for green color and create a mask
    lower_green = np.array([50, 100, 100]) # Example range, adjust based on your needs
    upper_green = np.array([70, 255, 255]) # Example range, adjust based on your needs
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Optional: Apply morphological operations to reduce noise, if necessary
    # kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Step 4: Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    points = []
    # Step 5: Extract coordinates
    for cnt in contours:
        # Calculate the centroid of the contour
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"Laser point at: ({cx}, {cy})")
            # Optional: Draw a circle at the centroid in the original image
            cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)
            points.append((cx, cy))
    
    return image, points
