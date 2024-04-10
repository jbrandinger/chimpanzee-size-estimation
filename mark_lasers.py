#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 15 2024

@author: jbrandinger

NAME: mark_lasers.py

PURPOSE: 
    - label images with input coordinates for SAM

HOW TO USE:
    - change appropriate folder paths and output file destinations
    - run script with 'python3 label.py'
    - image will pop up, click where you want the input label and then hit the
      'n' key to proceed to the next image

NOTES:
    - be sure to select central point that is not on laser pointers as
      SAM will segment the lasers
"""

# imports
import cv2
import os
import json

# path to folder containing the images
image_folder = 'sample_data/red_lasers/sample_data'

# json file to store results
output_file = 'sample_data/red_lasers/sample_data_truth.json'

# dictionary that will be converted to json
image_data = {}

# current image
current_image_name = ""

# track the number of clicks per image
click_count = 0

def click_event(event, x, y, flags, params):
    global current_image_name, click_count
    if event == cv2.EVENT_LBUTTONDOWN:
        click_count += 1
        print(f"Coordinates: (x={x}, y={y})")

        # Initialize data structure if not present
        if current_image_name not in image_data:
            image_data[current_image_name] = {'laser_points': [], 'body_points': []}

        # First and second clicks for laser points
        if click_count == 1 or click_count == 2:
            image_data[current_image_name]['laser_points'].append((x, y))
        # Third and fourth clicks for body points
        elif click_count == 3 or click_count == 4:
            image_data[current_image_name]['body_points'].append((x, y))

        # Reset clicks after fourth click and prompt for next image
        if click_count == 4:
            print("Press 'n' to proceed to the next image.")
            click_count = 0  # Reset click count for the next image

# iterate through folder
for image_name in os.listdir(image_folder):
    # Reset click count for each new image
    click_count = 0
    print(image_name)
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, image_name)
        current_image_name = image_name

        # display image
        img = cv2.imread(image_path)
        cv2.imshow(image_name, img)

        # set mouse callback function to capture clicks
        cv2.setMouseCallback(image_name, click_event)

        # wait until 'n' key is pressed to continue
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('n'):
                break

        cv2.destroyAllWindows()

# write image data to json file
with open(output_file, 'w') as file:
    json.dump(image_data, file, indent=4)

print(f"Data saved to {output_file}")
