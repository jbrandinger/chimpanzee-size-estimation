#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 15 2024

@author: jbrandinger

NAME: label.py

PURPOSE: 
    - label images with input coordinates for SAM

HOW TO USE:
    - change appropriate folder paths and output file destinations
    - run script with 'python3 label.py'
    - image will pop up, click where you want the input label and then hit the
      'n' key to proceed to the next image
"""

# imports
import cv2
import os
import json

# path to folder containing the images
image_folder = 'sample_data'

# json file to store results
output_file = 'im_coords.json'

# dictionary that will be converted to json
image_data = {}

# current image
current_image_name = ""

def click_event(event, x, y, flags, params):
    global current_image_name
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: (x={x}, y={y})")
        # add coordinates to dictionary
        image_data[current_image_name] = {'x': x, 'y': y}
        print("Press 'n' to proceed to the next image.")

# iterate through folder
for image_name in os.listdir(image_folder):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, image_name)
        current_image_name = image_name

        # display image
        img = cv2.imread(image_path)
        cv2.imshow(image_name, img)

        # set mouse callback function to capture click
        cv2.setMouseCallback(image_name, click_event)

        # wait until 'n' key is pressed to continue
        while True:
            # cv2.waitKey(0) will wait indefinitely for a key press
            key = cv2.waitKey(0) & 0xFF
            if key == ord('n'):
                break

        cv2.destroyAllWindows()

# write image data to json file
with open(output_file, 'w') as file:
    json.dump(image_data, file, indent=4)

print(f"Data saved to {output_file}")

