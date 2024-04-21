import os
import shutil
import pandas as pd

# Paths
source_folder_path = '../../data/QC'
spreadsheet_path = '../../data/measured.csv'
valid_destination_folder_path = '../../data/valid_QC'
invalid_destination_folder_path = '../../data/invalid_QC'

# Read the spreadsheet to get image names
spreadsheet_df = pd.read_csv(spreadsheet_path)
names_column = set(spreadsheet_df['PhotoID'])

# Ensure the destination folders exist
if not os.path.exists(valid_destination_folder_path):
    os.makedirs(valid_destination_folder_path)
if not os.path.exists(invalid_destination_folder_path):
    os.makedirs(invalid_destination_folder_path)

# Process images
matched_images = []
unmatched_images = []
num = 0
for root, dirs, files in os.walk(source_folder_path):
    for file in files:
        num += 1
        name = str(file).split('.')[0]
        file_path = os.path.join(root, file)
        if name in names_column:
            matched_images.append(file_path)
        else:
            unmatched_images.append(file_path)

# Copy matched images to the valid directory
for file_path in matched_images:
    shutil.copy2(file_path, valid_destination_folder_path)

# Copy unmatched images to the invalid directory
for file_path in unmatched_images:
    shutil.copy2(file_path, invalid_destination_folder_path)

print(f"Number of matched images: {len(matched_images)}/{num}")
print(f"Number of unmatched images: {len(unmatched_images)}/{num}")
