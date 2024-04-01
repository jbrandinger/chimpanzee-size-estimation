'''
chimparison2.py
'''

# necessary imports
import os
import pandas as pd

import shutil

# helper function to remove '.jpg' labels
def clean_image(image):
    cleaned_image = image[:(len(image)-4)]
    return cleaned_image

folder_path = '../../data/'

images = []
for root, dirs, files in os.walk(folder_path):
        for file in files:
            images.append(clean_image(str(file).lower()))

# get names of images in spreadsheet
spreadsheet_df = pd.read_csv('../../measured.csv')
names_column = spreadsheet_df['PhotoID']
names_column_cleaned = []
for image in names_column:
    names_column_cleaned.append(str(image).lower())
# print(names_column_cleaned)

collected_images = []
for im in images:
    if im in names_column_cleaned:
        collected_images.append(im)

print("Number of matched images: " + str(len(collected_images)))
print("Ratio of matched images: " + str(len(collected_images)) + "/" + str(len(images)))
# print(collected_images)

# for image in collected_images:
#     shutil.copy(image, './destination2')