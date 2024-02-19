import cv2
import numpy as np


def find_lasers(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Debugging: Display the mask to check if the laser points are detected
    cv2.imshow('Mask', mask)
    cv2.waitKey(0)  # Wait for a key press to close the displayed window

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Number of contours found: {len(contours)}")  # Debugging line

    # Assuming laser points are among the largest red spots detected:
    # Sort contours by area and keep the two largest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    points = []
    print("here1")
    # Step 5: Extract coordinates of the two largest contours
    for cnt in contours:
        print("here")
        # Calculate the centroid of the contour
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"Red laser point at: ({cx}, {cy})")
            # Optional: Draw a circle at the centroid in the original image
            cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)
            points.append((cx, cy))

    return image, points
