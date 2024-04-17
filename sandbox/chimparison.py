'''
chimparison2.py
'''

import os
import shutil
import pandas as pd

# Paths
source_folder_path = '../../data/QC'
spreadsheet_path = '../../data/measured.csv'
destination_folder_path = '../../data/valid_QC'

# Read the spreadsheet to get image names
spreadsheet_df = pd.read_csv(spreadsheet_path)
names_column = list(spreadsheet_df['PhotoID'])

# Ensure the destination folder exists
if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)

# Collect matched images and their paths
collected_images = []
for root, dirs, files in os.walk(source_folder_path):
    for file in files:
        name = str(file).split('.')[0]
        if name in names_column:
            # Append the file path to the list
            collected_images.append(os.path.join(root, file))

# Copy matched images to the new directory
for file_path in collected_images:
    shutil.copy2(file_path, destination_folder_path)

print("Number of matched images: " + str(len(collected_images)))
print("Ratio of matched images: " + str(len(collected_images)) + "/" + str(len(names_column)))

