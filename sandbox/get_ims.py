import os
import shutil

def find_and_copy_images(src_dir, dst_dir, image_names):
    """
    Copies images from the source directory to the destination directory.

    Args:
    src_dir (str): The path to the directory where to search for images.
    dst_dir (str): The path to the directory where to copy the images.
    image_names (list): A list of image filenames to search for and copy.
    """
    # Check if the destination directory exists, if not, create it
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    count = 0
    # Iterate through all files in the source directory
    for filename in os.listdir(src_dir):
        file = filename.split('.')[0]
        if file in image_names:
            src_path = os.path.join(src_dir, filename)
            dst_path = os.path.join(dst_dir, filename)
            # Copy each found image to the destination directory
            shutil.copy(src_path, dst_path)
            count += 1
    print(f"Copied {count} of {len(image_names)} images")

# Example usage:
source_directory = '../../data/valid_QC'
destination_directory = '../../data/laser_fail'
image_list = ['25-Jan-2016-312',
 '23-Nov-2015-1',
 '10_Nov_2015-386',
 '13-Nov-2015-45',
 '8-Feb-2016-184',
 '2-Dec-2015-86',
 '1-Dec-2015-137',
 '13-Nov-2015-99',
 '17-Nov-2015-415',
 '1-Dec-2015-153']

find_and_copy_images(source_directory, destination_directory, image_list)
