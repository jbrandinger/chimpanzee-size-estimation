#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on April 02 2024

@author: jbrandinger

NAME: pipeline.py

PURPOSE: 
    - run entire image processing pipeline

HOW TO USE:
    - run script with 'python3 pipeline.py'
NOTES:
    - this script assumes that 'label.py' has already been ran to get input
      points for all images
"""

##############################################################################
#                                  IMPORTS                                   #
##############################################################################
# basics
import numpy as np
import pandas as pd
import math
from tqdm import tqdm
# file work
import os
import json
# computer vision
import cv2
import laser_detection as ld
# models
from segment_anything import sam_model_registry, SamPredictor
from easy_ViTPose import VitInference
from huggingface_hub import hf_hub_download

##############################################################################
#                          PART 1: LOAD IMAGE DATA                           #
##############################################################################
# path to json file
json_file = 'all_data.json'
# folder containing images
image_folder = '../red_laser_data'

# load data
with open(json_file, 'r') as file:
    image_data = json.load(file)

print(f"Running {len(image_data)} images through pipeline")
##############################################################################
#                                 PART 2: SAM                                #
##############################################################################
# select checkpoint and model type
sam_checkpoint = "../sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"
# define predictor
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)

#function to generate mask
def generate_mask(im, input_point):
    input_label = np.array([1])
    predictor.set_image(im)
    masks, scores, _ = predictor.predict(point_coords=input_point, 
                                         point_labels=input_label, 
                                         multimask_output=True)
    # return best mask
    return masks[np.argmax(scores)]

# folder to place masks
mask_folder = 'red_lasers/new_sample_data_masks'
# Ensure mask folder exists
os.makedirs(mask_folder, exist_ok=True)

# iterate through each entry in the JSON data
for image_name, im_data in tqdm(image_data.items(), desc="SAM"):
    image_path = os.path.join(image_folder, image_name)
    
    # Load the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    if img is not None:
        # extract coordinates
        input_point = np.array([im_data['input_point']])
        # Generate the mask
        mask = generate_mask(img, input_point)
        mask = mask.astype(np.uint8)
        
        # Define the mask filename
        mask_filename = os.path.splitext(image_name)[0] + "_mask.png"
        mask_path = os.path.join(mask_folder, mask_filename)
        
        # Save the mask
        cv2.imwrite(mask_path, mask)
        
        # Update the JSON data with the mask filename
        image_data[image_name]['mask'] = mask_filename

##############################################################################
#                        PART 3: LASER POINT DETECTION                       #
##############################################################################
# iterate through each entry in json
for image_name, info in tqdm(image_data.items(), desc="Laser Point Detection"):
    image_path = os.path.join(image_folder, image_name)
    # load image
    source = cv2.imread(image_path)

    # Load the mask
    mask_filename = info['mask']
    mask_path = os.path.join(mask_folder, mask_filename)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)  # Load mask in grayscale

    mask = mask > 0  # need to convert to boolean values

    if source is not None:
        # run laser detection image
        points = ld.detect_laser_points(source, mask)
        if len(points) < 2:
            print("Less than two lasers detected. Retrying without mask...")
            points = ld.detect_laser_points(source, 
                                            np.ones(source.shape, dtype=bool))
            print(f"Detected {len(points)} points without mask")
        
        # Update the JSON data with the mask filename
        image_data[image_name]['laser_points'] = points

##############################################################################
#                               PART 4: VITPOSE                              #
##############################################################################
# define model parameters
MODEL_SIZE = 'b'
YOLO_SIZE = 'n'
DATASET = 'apt36k'
ext = '.pth'
ext_yolo = '.pt'

# download model_path and yolo_path
MODEL_TYPE = "torch"
YOLO_TYPE = "torch"
REPO_ID = 'JunkyByte/easy_ViTPose'
FILENAME = os.path.join(MODEL_TYPE, 
                        f'{DATASET}/vitpose-' + MODEL_SIZE + f'-{DATASET}') + ext
FILENAME_YOLO = 'yolov8/yolov8' + YOLO_SIZE + ext_yolo
print(f'Downloading model {REPO_ID}/{FILENAME}')
model_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
yolo_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME_YOLO)

# initialize model
model = VitInference(model_path, yolo_path, MODEL_SIZE, dataset=DATASET)

# iterate through each entry in json
for image_name, info in tqdm(image_data.items(), desc="ViTPose"):
    image_path = os.path.join(image_folder, image_name)
    # load image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for plotting

    # get keypoints
    img_arr = np.array(img, dtype=np.uint8)
    keypoints = model.inference(img_arr)

    if keypoints:
      # store results
      shoulder = keypoints[0][3]
      shoulder = [int(shoulder[1]), int(shoulder[0])]
      rump = keypoints[0][4]
      rump = [int(rump[1]), int(rump[0])]
      # Update the JSON data with shoulder and rump
      image_data[image_name]['shoulder_rump'] = [shoulder, rump]
    else:
      print(f"vitpose failed for {image_path}")
      # TODO how do we want to handle this case in the json?
      image_data[image_name]['shoulder_rump'] = None

##############################################################################
#                      PART 5: GET FINAL DISTANCES                           #
##############################################################################
measured_df = pd.read_csv('../measured.csv')
measured_df = measured_df.dropna(subset=['PhotoID'])
conversion_dict = dict(zip(measured_df['PhotoID'], measured_df['Laser Width']))
true_dist_dcit = dict(zip(measured_df['PhotoID'], measured_df['BodyLength1']))

# iterate through each entry in json
for image_name, info in tqdm(image_data.items(), desc="Calculating Final Distances"):
    # distances in pixels
    laser_points = info['laser_points']
    shoulder_rump = info['shoulder_rump']

    # assert we have values
    if laser_points is None or shoulder_rump is None:
        continue
    
    # calculate ratio
    laser_dist = round(math.dist(points[0], points[1]), 3)
    sr_dist = round(math.dist(shoulder_rump[0], shoulder_rump[1]), 3)
    ratio = laser_dist / sr_dist
    
    # lookup laser width
    id = image_name.split('.')[0]
    laser_width = conversion_dict[id]
    body_length = laser_width / ratio
    print(f"Calculated length: {round(body_length, 3)}\tactual length: {round(true_dist_dcit[id], 3)}")
    
    
    
    
# Write the updated JSON data to a file
with open(json_file, 'w') as file:
    json.dump(image_data, file, indent=4)

print(f"Updated data saved to {json_file}")
